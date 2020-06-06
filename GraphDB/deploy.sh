# Script / Commands used to deploy neo4j on AWS.

# Create key pair
export KEY_NAME="Neo4j-AWSMarketplace-Key"
aws ec2 create-key-pair \
  --key-name $KEY_NAME \
  --query 'KeyMaterial' \
  --output text > $KEY_NAME.pem \
  --profile ucsd \
  --region us-east-1

# Create Security Group
export GROUP="neo4j-sg"
aws ec2 create-security-group \
  --group-name $GROUP \
  --description "Neo4j security group" \
  --profile ucsd \
  --region us-east-1

# open neo4j ports
for port in 22 7474 7473 7687; do
  aws ec2 authorize-security-group-ingress --group-name $GROUP --protocol tcp --port $port --cidr 0.0.0.0/0 --profile ucsd --region us-east-1
done

# describe images for neo4j type
aws ec2 describe-images \
   --region us-east-1 \
   --owner 385155106615 \
   --query "Images[*].{ImageId:ImageId,Name:Name}" \
   --profile ucsd \
   --region us-east-1

# deploy neo4j image
aws ec2 run-instances \
  --image-id ami-00399c91e340d0bfa \
  --count 1 \
  --instance-type m3.medium \
  --key-name $KEY_NAME \
  --security-groups $GROUP \
  --query "Instances[*].InstanceId" \
  --profile ucsd \
  --region us-east-1

# desscribe imstance
aws ec2 describe-instances \
  --instance-ids [InstanceId] \
  --query "Reservations[*].Instances[*].PublicDnsName" \
  --profile ucsd \
  --region us-east-1

# chmod 600 $KEY_NAME.pem
scp -i $KEY_NAME.pem ~/Desktop/neo4j-graph-algorithms-3.5.14.0-standalone.jar ubuntu@ec2-3-84-117-118.compute-1.amazonaws.com:~/.
ssh -i $KEY_NAME.pem ubuntu@ec2-3-84-117-118.compute-1.amazonaws.com

#  neo4j home: /var/lib/neo4j
export NEO4J_HOME="/var/lib/neo4j"