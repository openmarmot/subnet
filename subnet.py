
'''
module : subnet.py
Language : Python 3.x
email : andrew@openmarmot.com
notes : subnet math. loosely based on how i learned to do this 
manually for the Cisco CCNA exam.
may contain errors..
'''

#import built in modules

#import custom packages

#--------------------------------------------------
def main():
    while True:
        print('OpenMarmot Subnet Calculator')
        print('0 - Exit')
        print('1 - Convert CIDR to Subnet Mask')
        print('2 - Covert Subnet Mask to CIDR')
        print('3 - Determine the subnet a CIDR IP belongs to')
        selection=input('Enter selection: ')
        
        if selection=='0':
            print('Goodbye!')
            break
        elif selection=='1':
            value=input('Enter a CIDR Network Number [xx]:')
            result=cidr_to_subnet(value)
            print('Result: ',result)
        elif selection=='2':
            value=input('Enter a Subnet Mask [xxx.xxx.xxx.xxx]:')
            result=subnet_to_cidr(value)
            print('Result: ',result)
        elif selection=='3':
            value=input('Enter a CIDR IP [x.x.x.x/x]:')
            result=get_network(value)
            print('Result: ',result)
        
#--------------------------------------------------

#--------------------------------------------------
def cidr_to_subnet(CIDR):
    ''' converts a CIDR (int) to a subnet (string) '''
    octet1=[1,2,3,4,5,6,7,8]
    octet2=[9,10,11,12,13,14,15,16]
    octet3=[17,18,19,20,21,22,23,24]
    octet4=[25,26,27,28,29,30,31,32]

    bitChart=[128,192,224,240,248,252,254,255]

    subnet=''
    #convert to int if it wasn't already
    CIDR=int(CIDR)
    if CIDR in octet1:
        subnet=str(bitChart[octet1.index(CIDR)])+'.0.0.0'
    elif CIDR in octet2:
        subnet='255.'+str(bitChart[octet2.index(CIDR)])+'.0.0'
    elif CIDR in octet3:
        subnet='255.255.'+str(bitChart[octet3.index(CIDR)])+'.0'
    elif CIDR in octet4:
        subnet='255.255.255.'+str(bitChart[octet4.index(CIDR)])
    else:
        print('Error : variable supplied is out of range for CIDR ',CIDR)

    return subnet

#--------------------------------------------------
def get_significant_octet(subnet_mask,programmer_notation=True):
    ''' returns what octet of a subnet mask is significant '''
    # programmer_notation - numbers start at zero not one
    subnet_mask=subnet_mask.split('.')
    octet=None
    if subnet_mask[0]!='255':
        octet=1
    elif subnet_mask[1]!='255':
        octet=2
    elif subnet_mask[2]!='255':
        octet=3
    elif subnet_mask[3]!='255':
        octet=4
    else:
        print('error : subnet mask has zero network bits')
            
    if programmer_notation:
        octet-=1
    return octet
    
#--------------------------------------------------
def subnet_to_cidr(subnet):
    ''' converts a subnet (string) to CIDR format (returns int) '''
    octets=[[1,2,3,4,5,6,7,8],[9,10,11,12,13,14,15,16],
        [17,18,19,20,21,22,23,24],[25,26,27,28,29,30,31,32]]
    bitChart=[128,192,224,240,248,252,254,255]
    significant_octet=get_significant_octet(subnet)
    subnet=subnet.split('.')
    return str(octets[significant_octet][bitChart.index(int(subnet[significant_octet]))])

#--------------------------------------------------
def get_network(CIDR):
    ''' returns the network address a CIDR belongs to '''
    ip,mask=CIDR.split('/')
    binary_mask=cidr_to_subnet(mask)
    significant_octet=get_significant_octet(binary_mask)
    increment=256-int(binary_mask.split('.')[significant_octet])
    net_value=int(ip.split('.')[significant_octet])
    sub_start=0
    sub_end=0
    # generate subnets until we find the right one
    while True:
        sub_end=sub_start+increment-1
        #determine if we are in the correct subnet
        if sub_end>=net_value:
            break
        sub_start=sub_end+1
    ip=ip.split('.')
    networkCIDR=''
    broadcastAddress=''
    if significant_octet==0:
        networkCIDR=str(sub_start)+'.0.0.0/'+mask
        broadcastAddress=str(sub_end)+'.255.255.255'
    elif significant_octet==1:
        networkCIDR=ip[0]+'.'+str(sub_start)+'.0.0/'+mask
        broadcastAddress=ip[0]+'.'+str(sub_end)+'.255.255'
    elif significant_octet==2:
        networkCIDR=ip[0]+'.'+ip[1]+'.'+str(sub_start)+'.0/'+mask
        broadcastAddress=ip[0]+'.'+ip[1]+'.'+str(sub_end)+'.255'
    elif significant_octet==3:
        networkCIDR=ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(sub_start)+'/'+mask
        broadcastAddress=ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(sub_end)

    return {'network':networkCIDR,'broadcast address':broadcastAddress,'network increment':str(increment)}
    

main()
