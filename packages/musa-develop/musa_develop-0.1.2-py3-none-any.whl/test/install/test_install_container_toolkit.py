from test.utils import set_env, TestInstall  # noqa
from musa_develop.install.install import ContainerToolkitsPkgMgr


# TODO: sudo /home/gl/miniconda3/envs/py310/bin/pytest  --capture=no -v  ./test/install/test_install_container_toolkit.py::test_install_container_toolkit_with_intranet
# 不带上--capture=no -v 参数, 在安装container_toolkit 时由于log 被捕捉不显示, 会卡在中间环境
@set_env({"DOWNLOAD_IN_HOST_TEST": "True"})
def test_install_container_toolkit_with_intranet():
    test_install = TestInstall(ContainerToolkitsPkgMgr)
    test_install.install()
    test_install.set_version_ground_truth(
        mtml="1.9.2-linux",
        sgpu_dkms="1.2.1",
        mt_container_toolkit="1.9.0-1",
    )
    test_install.check_is_installed_success_with_version()
    test_install.check_work_after_install()


@set_env({"DOWNLOAD_IN_HOST_TEST": "False"})
def test_install_container_toolkit_with_extranet():
    test_install = TestInstall(ContainerToolkitsPkgMgr)
    test_install.install()
    test_install.set_version_ground_truth(
        mtml="1.9.2-linux",
        sgpu_dkms="1.2.1",
        mt_container_toolkit="1.9.0-1",
    )
    test_install.check_is_installed_success_with_version()
    test_install.check_work_after_install()
