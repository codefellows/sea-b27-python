import time
import boto
from fabric.api import local, task, env, open_shell


env["user"] = "ec2-user"
env["key_filename"] = "~/.ssh/imagr"


def create_network():
    vpc_connection = boto.connect_vpc()
    vpc = vpc_connection.create_vpc("10.0.0.0/24")
    subnet = vpc_connection.create_subnet(vpc.id, "10.0.0.0/25")
    gateway = vpc_connection.create_internet_gateway()
    vpc_connection.attach_internet_gateway(gateway.id, vpc.id)
    return subnet.id


def create_server(subnet_id):
    ec2_connection = boto.connect_ec2()
    reservation = ec2_connection.run_instances("ami-b66ed3de",
                                               key_name="imagr",
                                               instance_type="t2.micro",
                                               subnet_id=subnet_id)
    print "Sleeping while EC2 nodes come up..."
    time.sleep(60)
    print "done\n"
    elastic_ip = ec2_connection.allocate_address(domain="vpc")
    ec2_connection.associate_address(instance_id=reservation.instances[0].id,
                                     allocation_id=elastic_ip.allocation_id)
    return elastic_ip.public_ip


@task
def checkpoint():
    local("python ./manage.py makemigrations")
    local("git add .")
    local("git commit")


@task
def deploy_node():
    # Note that open_shell was not working in the example we ran through
    subnet_id = create_network()
    node_ip = create_server(subnet_id)
    print node_ip
    env["hosts"] = [node_ip]
    open_shell()
