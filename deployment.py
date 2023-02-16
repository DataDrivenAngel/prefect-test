# deployment
from flow import pipe
from prefect.deployments import Deployment
from prefect.filesystems import GitHub

github_block = GitHub.load("github-storage")

deploy = Deployment.build_from_flow( flow = pipe
                                     , name = "fresh block storage test"
                                     , storage = github_block 
                                     )


if __name__ == "__main__":
    deploy.apply()



# manual
# 
# create deployment
# prefect deployment build deployment.py:pipe -n first_deployment -a
# start 
# prefect agent start -q 'default'
#

