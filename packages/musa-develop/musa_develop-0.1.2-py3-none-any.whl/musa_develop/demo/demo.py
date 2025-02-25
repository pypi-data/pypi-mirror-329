from abc import ABC, abstractmethod
from musa_develop.install import PACKAGE_MANAGER
from musa_develop.config.yaml_read import ImageYaml, ImageClass
from musa_develop.check.shell_executor import DockerShellExecutor
from musa_develop.check.utils import CheckModuleNames
from musa_develop.utils import GenerateContainerName, FontRed, SHELL, get_gpu_type

import os

from dataclasses import dataclass, field

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
IMAGE_FILE_PATH = os.path.join(CURRENT_FOLDER, "../config/")


# TODO(@caizhi): please read from yaml files
GLOBAL_TORCH_MUSA_DRIVER_MAP = {"1.3.1": "20241025"}
GLOBAL_VLLM_DRIVER_MAP = {"0.4.0": "20241025"}
NEWEST_DRIVER_VERSION = "20241025"


# 为了方便维护，将不同的应用分别赋值给2个list成员变量，代码匹配列表元素作为任务，但是暂不提供接口修改列表
# 后续如果有新的task，直接在该类中的列表增加元素即可；后续若需要新的容器，增加成员变量即可
@dataclass
class DemoTask:
    torch_task: list = field(
        default_factory=lambda: ["base", "train_cifar10", "resnet50", "yolov5"]
    )
    vllm_task: list = field(default_factory=lambda: ["qwen2-0.5b"])

    def get_all_task(self) -> list:
        return self.torch_task + self.vllm_task


class BaseDemoDeployer(ABC):

    def __init__(self) -> None:
        self._version = None
        self._task: str = None
        self._installer = list()
        self._use_docker = False
        self._image = None
        self._driver_installer = PACKAGE_MANAGER[CheckModuleNames.driver.name]
        self._container_toolkit_installer = PACKAGE_MANAGER[
            CheckModuleNames.container_toolkit.name
        ]

        self._status: bool = False
        self._image_args = ImageClass()
        self._image_reader = ImageYaml(IMAGE_FILE_PATH)
        self._task_list = DemoTask()
        self._docker_shell = None
        self._target_driver_version = None

    def prepare_dependency(self):
        pass

    def prepare_demo_shell(self):
        pass

    def run_demo_shell(self):
        pass

    def get_docker_image(self, img_tag: str = None) -> str:
        # image_str = None
        # self.perpare_img_arg(img_tag)
        # image_str = self._image_reader.get_image_name(self._image_args)
        # return image_str
        pass

    def perpare_img_arg(self, img_tag: str = None) -> None:
        """Prepare the image arguments with the specified tag and type.

        Args:
            img_type(str): type of docker image, such as 'torch_musa', 'mtt-vllm'
            img_tag(str):
        """
        # 针对仅启动一个开发容器，用torch_musa作为开发容器，因为torch_musa容器有driver信息
        # 维护列表，将相同容器类型的任务放在同一个列表中
        if self._task in self._task_list.torch_task:
            if not img_tag:
                self._image_args.image_tag = "py310"  # torch_musa默认tag为py310
            else:
                self._image_args.image_tag = img_tag
            self._image_args.image_type = "torch_musa"
        elif self._task in self._task_list.kuae_task:
            # 如果是kuae容器，不需要tag
            if img_tag:
                print(
                    f"The container of {self._task} task don't need image tag, \
                        please remove the '--tag' parameter and run again"
                )
                exit()
            self._image_args.image_type = "mtt-vllm"
        else:
            print(
                "The application is not integrated in MUSA-Develop, \
                please run 'musa-develop -h' to see how to use it"
            )
            exit()

    def start_container(
        self,
        container_name: str = None,
        workdir: str = None,
        host_dir: str = None,
        container_dir: str = None,
    ) -> bool:
        """Start a container to run the AI applications

        Args:
            img_name (str): docker image name, obtained by the get_img_name() function

        Returns:
            True: start container success
            False: start container failed
        """
        # 不同的task虽然容器不同但是启动方式相同
        # TODO：需要更改create_container接口
        self._docker_shell.create_container(
            image_name=self._image,
            workdir=workdir,
            host_dir=host_dir,
        )
        status = True

        return status

    @abstractmethod
    def set_installer(self):
        pass

    def get_driver_requirement(self):
        pass

    def set_docker_image_requirement(self):
        pass

    def set_driver_target_version(self):
        if self._version:
            if self._demo == "torch_musa":
                self._target_driver_version = GLOBAL_TORCH_MUSA_DRIVER_MAP[
                    self._version
                ]
            elif self._demo == "vllm":
                self._target_driver_version = GLOBAL_VLLM_DRIVER_MAP[self._version]
            else:
                print(FontRed("==========wrong demo ==============!"))
                exit()
        else:
            self._target_driver_version = None

    def start(
        self,
        version: str,
        task: str,
        use_docker: bool,
        container_name: str = None,
        workdir: str = None,
        host_dir: str = None,
        container_dir: str = None,
        img_tag: str = None,
    ) -> bool:
        self._version = version
        self._task = task
        self._use_docker = use_docker
        self.set_installer()

        # 1. prepare dependency environment
        if self._use_docker:
            # 1.1 set dependency driver version
            self.set_driver_target_version()
            # 1.2 set driver version in container_toolkit_installer
            self._container_toolkit_installer.set_driver_target_version(
                self._target_driver_version
            )
            # 1.3 install container_toolkits
            need_reboot = self._container_toolkit_installer.install()
            if need_reboot:
                return True
        else:
            # ===================
            pass

        # 2. start docker if need
        if self._use_docker:
            # 2.1 get image name
            self.set_docker_image_requirement()
            if not self._image:
                print(
                    FontRed(
                        f"No suitable image was found for the current task {self._demo} : {self._task}!"
                    )
                )
                return
            # 2.2 get container name
            if not container_name:
                container_name = GenerateContainerName(self._demo, self._task)
            # 2.3 start docker container
            self._docker_shell = DockerShellExecutor(container_name)
            container_start_status = self.start_container(container_name)
            if not container_start_status:
                return

        # 3. prepare demo code for task
        self.set_demo_shell()

        # 4. run demo code
        if not self._use_docker:
            SHELL().run_cmd(f"bash {self._demo_shell}")
        else:
            # TODO(@wangkang): 优化
            # self._docker_shell.send_container_cmd(self._demo_shell)
            SHELL().run_cmd(
                f"docker exec -it {container_name} /bin/bash -c 'source ~/.bashrc; {self._demo_shell}'"
            )


class TorchMusaDeployer(BaseDemoDeployer):
    def __init__(self) -> None:
        super().__init__()
        self._demo = CheckModuleNames.torch_musa.name

    def set_installer(self):
        if not self._use_docker:
            self._installer = PACKAGE_MANAGER[CheckModuleNames.torch_musa.name]

    def set_docker_image_requirement(self):
        if self._use_docker:
            # get gpu type
            gpu_type = get_gpu_type()
            # TODO(@caizhi): lookup table and get right image
            if gpu_type == "mp_21":
                self._image = "sh-harbor.mthreads.com/mt-ai/musa-pytorch-dev-py38:rc3.1.0-v1.3.0-qy1"
            else:
                self._image = "sh-harbor.mthreads.com/mt-ai/musa-pytorch-dev-py38:rc3.1.0-v1.3.0-qy2"
                # # 获取img_name,通过task，gpu_type等变量从yaml中获取镜像名
                # img = self.get_image(img_tag)

    def set_demo_shell(self):
        if self._task == "base":
            self._demo_shell = ":"
        elif self._task == "train_cifar10":
            self._demo_shell = "git clone https://github.com/MooreThreads/tutorial_on_musa.git && cd tutorial_on_musa/pytorch/QuickStart/ && python train_cifar10.py 2>&1|tee GGN-train_cifar10.log"
        elif self._task == "yolov5":
            self._demo_shell = ":"
        else:
            print("No task is specified.")
            self._demo_shell = ":"


class vLLMDeployer(BaseDemoDeployer):
    def __init__(self) -> None:
        super().__init__()
        self._demo = CheckModuleNames.vllm.name

    def set_installer(self):
        if not self._use_docker:
            self._installer = PACKAGE_MANAGER[CheckModuleNames.vllm.name]

    def set_docker_image_requirement(self):
        if self._use_docker:
            # get gpu type
            self._image = (
                "registry.mthreads.com/mcconline/mtt-vllm-public:v0.2.0-kuae1.3.0"
            )
            # # 获取img_name,通过task，gpu_type等变量从yaml中获取镜像名
            # img = self.get_image(img_tag)

    def set_demo_shell(self):
        if self._task == "base":
            self._demo_shell = ":"
        elif self._task == "qwen2-0.5b":
            self._demo_shell = "git clone https://github.com/MooreThreads/tutorial_on_musa.git && cd tutorial_on_musa/vllm/check_vllm_image && bash ./vllm_check.sh 2>&1|tee vllm_qwen2_0.5b.log"
        else:
            print("No task is specified.")
            self._demo_shell = ":"
