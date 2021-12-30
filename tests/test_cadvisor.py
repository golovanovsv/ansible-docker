# Disabled. See in ../molecule/default/vars.yml
# import testinfra
# import urllib.request
# from pprint import pprint

# def test_cadvisor_is_running(host):
#   assert host.docker("cadvisor").is_running

# def test_cadvisor_is_listening(host):
#   assert host.socket("tcp://0.0.0.0:8081").is_listening

# TODO: test /healthz endpoint
# def test_cadvizor_health_check(host):
#   url = "http://{}:8081/healthz".format(host.interface("eth0").addresses[0])
#   print(url)
#   print(urllib.request.urlopen( "http://{}:8080/healthz".format("172.23.128.2") ))
#   assert urllib.request.urlopen("http://{}:8081/healthz".format(host.Addr.ipv4_addresses))
