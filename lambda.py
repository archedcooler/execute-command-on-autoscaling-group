import boto3
import json
import random
import time

region = 'us-east-1'

ec2 = boto3.client('ec2', region_name=region)
ssm_client = boto3.client('ssm')

def execute_script(instance, command):
    
    run_command = str(command)
    
    print('Running AWS-RunShellScript on '+ instance)
    
    print("Running Command: " + run_command)
    
    #This client is using the Document AWS-RunShellScript which is meant for linux 
    ssm_response = ssm_client.send_command(
    InstanceIds=[instance],
    DocumentName='AWS-RunShellScript',
    Parameters={
        'commands': [run_command]
    })
    
    command_id = ssm_response['Command']['CommandId']
    
    time.sleep(2)
    
    output = ssm_client.get_command_invocation(
      CommandId=command_id,
      InstanceId=instance,
    )
    print(output)
    print ('-' * 20)


def lambda_handler(event, context):
    
    #Insert command you would like to run on server here
    command = 'Insert Command here'
    
    print ('-' * 20)    
    print('Running Run-CronJobs-Prod Lambda Script')
    print ('-' * 20)

    #This command is filtering on the tag where Name = <NameOfAutoScalingGroup>. 
    response = ec2.describe_instances(Filters=[{
                                                'Name':'tag:Name',
                                                'Values': ['NameOfAutoScalingGroup'
                                                ]},
                                                {
                                                'Name':'instance-state-name',
                                                'Values': ['running'
                                                ]}
                                                ])['Reservations']
    
    instances = []
    
    print('Listing Running Instances:')
    for reservation in response:
        
        
        for instance in reservation['Instances']:
            
            instances.append(instance)
            print("Running Instance Image ID: {} Running instance Instance Type: {} Running Instance Keyname {}"
            .format(instance['InstanceId'],instance['InstanceType'],instance['KeyName']))
    
        
    randomInstance = random.choice(instances)
    
    randomInstanceId = randomInstance['InstanceId']
    
    print ('-' * 20)
    print ("The selected instance is: " + randomInstanceId)
    print ('-' * 20)
    
    execute_script(randomInstanceId,command)
    


    
    