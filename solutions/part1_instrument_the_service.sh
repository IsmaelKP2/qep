#!/bin/bash

# This setup script will:
# (1) Build the credit-check-service app
# (2) Export the image from docker
# (3) Import it into k3s
#     (Steps 2 and 3 are so we don't need to use a public registry)
# (4) Deploy the service in kubernetes
# (5) Find and delete the pod (so it is redeployed)
#
# (1) Build the credit-check-service app
docker build -t credit-check-service-part1:latest part1 -f part1/Dockerfile.solutions1

# (2) Export the image from docker
docker save --output credit-check-service-part1.tar credit-check-service-part1:latest

# (3) Import it into k3s
sudo k3s ctr images import credit-check-service-part1.tar

# (5) Find and delete the pod (so it is redeployed)
podlist=$(kubectl get pods)
re="(creditcheckservice[^[:space:]]+)"
if [[ $podlist =~ $re ]]; then
  POD=${BASH_REMATCH[1]};
  echo "Restarting creditcheckservice pod:"
  kubectl delete po $POD
fi

echo ""
echo Redeployed creditcheckservice.

#add hostname in the yaml file
sed -i "s/{{addhost}}/$HOSTNAME/" part1/creditcheckservice-solutions-part1.yaml
#deploy the pod from credicheckservice-solutions.yaml 
kubectl apply -f part1/creditcheckservice-solutions-part1.yaml
