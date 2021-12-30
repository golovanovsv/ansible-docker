import testinfra
import pytest

@pytest.fixture()
def AnsibleVars(host):
  default_vars = host.ansible("include_vars", "file=defaults/main.yml")["ansible_facts"]
  test_vars = host.ansible("include_vars", "file=molecule/default/vars.yml")["ansible_facts"]
  merged_vars = { **default_vars, **test_vars }
  return merged_vars

def test_service_is_enabled(host):
  assert host.service("docker").is_enabled

def test_service_is_running(host):
  assert host.service("docker").is_running

def test_docker_config_is_exist(host):
  assert host.file("/etc/docker/daemon.json").is_file

def test_docker_config_content(host):
  config = host.file("/etc/docker/daemon.json").content_string
  assert '"log-driver": "json-file"' in config
  assert '"max-size": "200m"' in config

def test_docker_config_proxy(host):
  config = host.file("/lib/systemd/system/docker.service.d/proxy.conf")
  assert config.is_file
  assert config.user == "root"
  assert config.group == "root"
  assert oct(config.mode) == "0o644"

def test_docker_config_proxy_content(host, AnsibleVars):
  config = host.file("/lib/systemd/system/docker.service.d/proxy.conf").content_string
  assert f"HTTP_PROXY={AnsibleVars['proxy_server']}" in config
  assert f"HTTPS_PROXY={AnsibleVars['proxy_server']}" in config
  no_proxy = "127.0.0.1,localhost"
  for entry in AnsibleVars["proxy_ignores"]:
    no_proxy = f"{no_proxy},{entry}"
  assert f"NO_PROXY={no_proxy}" in config

def test_docker_socket_is_listening(host):
  # testinfra производит проверку при помощи ss/netstat, а у некоторых дистрибутивов /var/run/docker.sock
  #   является хардлинком на /run/docker.sock
  # Так же assert host.socket("unix:///var/run/docker.sock").is_listening or host.socket("unix:///run/docker.sock").is_listening
  #   не работает для ubuntu-1804 поэтому просто проверим, что /var/run/docker.sock есть и это сокет :/
  assert host.file("/var/run/docker.sock").is_socket

def test_docker_compose_installed(host):
  packages = host.pip.get_packages()
  assert "docker-compose" in packages
