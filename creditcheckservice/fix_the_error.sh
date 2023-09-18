#add hostname in the yaml file
sed -i "s/{{addhost}}/$HOSTNAME/" creditcheckservice-solutions.yaml
#deploy the pod from credicheckservice-solutions.yaml 
kubectl apply -f creditcheckservice-solutions.yaml