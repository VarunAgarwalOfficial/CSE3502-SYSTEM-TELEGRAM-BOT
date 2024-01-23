import telebot
import psutil as ps
import time
import pymongo
from datetime import date



TOKEN = "2136297571:AAHpPMNX6Ji_KEONmkWzD0UtVL9_XRJVimU"
tb = telebot.TeleBot(TOKEN)



G = 1024 * 1024 * 1024
M = 1024 * 1024
MIN = 60
HOUR = 60 * 60
DAY = 60 * 60 * 24

BOT_INFO = "This is a BOT created by Varun Agarwal 19BCT0070 for ISAA Theory DA."

@tb.message_handler(commands=['info'])
def send_info(msg):
    tb.reply_to(msg, BOT_INFO)
    mydb["info"].insert_one({"LOG_TIME":str(date.today())})

@tb.message_handler(commands=['uptime'])
def send_uptime(msg):
    res = "System uptime : \n"
    uptime = time.time() - ps.boot_time()
    days = int(uptime / DAY)
    hours = int((uptime - days * DAY) / HOUR)
    mins = int((uptime - days * DAY - hours * HOUR) / MIN)
    secs = int((uptime - days * DAY - hours * HOUR - mins * MIN) / 1)

    res += "%s Day(s) %s Hour(s) %s Minute(s) %s Second(s)\n" % (days, hours, mins, secs)
    res += "\n Checked on : " + str(date.today())
    tb.reply_to(msg, res)
    mydb["uptime"].insert_one({"LOG_TIME":str(date.today()),"uptime":uptime})

@tb.message_handler(commands=['coretemp'])
def get_CPU_Core_Temp(msg):
    res = "CPU Temperature\n"
    temp = ps.sensors_temperatures()['coretemp']
    for i in range(0, len(temp)):
        res += " Core " + str(i + 1) + " : " + str(temp[i].current) + " ℃\n"
    tb.reply_to(msg, res)
    mydb["coretemp"].insert_one({"LOG_TIME":str(date.today()),"coretemp":res})


@tb.message_handler(commands=['mem'])
def get_MEM_Info(msg):
    res = "Memory Info\n"
    tol_swap = ps.swap_memory().total
    avail_swap = ps.swap_memory().free
    swap_percent = ps.swap_memory().percent
    tol_mem = ps.virtual_memory().total
    avail_mem = ps.virtual_memory().available
    mem_percent = ps.virtual_memory().percent
    res += "Memory Usage: " + str(mem_percent) + "%\n"
    res += "Available: " + str(round(avail_mem / G, 2)) + "%\n"
    res += "Swap Usage: " + str(swap_percent)  + "%\n"
    res += "Available: " + str(round(avail_swap / G, 2)) + "%\n" 
    tb.reply_to(msg, res)
    mydb["meminfo"].insert_one({"LOG_TIME":str(date.today()),"meminfo":res})

@tb.message_handler(commands=['disk'])
def get_Disk_Info(msg):
    res = "Disk Info\n"
    partitions = ps.disk_partitions()
    for each in partitions:
        usage = ps.disk_usage(each.mountpoint)
        res += "\t" + each.mountpoint + " Usage: "
        res += str(usage.percent) + "%\n"
        res += "\t\tFree: " + str(round(usage.free / G, 2)) + "G\t"
        res += "\t\tUsed: " + str(round(usage.used / G, 2)) + "G\t"
        res += "\t\tTotal: " + str(round(usage.total / G, 2)) + "G\n"
    tb.reply_to(msg, res)
    mydb["diskinfo"].insert_one({"LOG_TIME":str(date.today()),"diskinfo":res})







@tb.message_handler(commands=['ip'])
def get_IP_Info(msg):
    res = "Network Information\n"
    if_addrs = ps.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            res += (f"Interface: {interface_name}\n")
            if str(address.family) == 'AddressFamily.AF_INET':
                res += (f"  IP Address: {address.address}\n")
                res += (f"  Netmask: {address.netmask}\n")
                res += (f"  Broadcast IP: {address.broadcast}\n")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                res += (f"  MAC Address: {address.address}\n")
                res += (f"  Netmask: {address.netmask}\n")
                res += (f"  Broadcast MAC: {address.broadcast}\n")
    tb.reply_to(msg, res)
    mydb["ipinfo"].insert_one({"LOG_TIME":str(date.today()),"ipinfo":res})

@tb.message_handler(commands=['cpu'])
def get_CPU_Info(msg):
    res = ("CPU Info")
    # number of cores
    res += ("Physical cores:" + str(ps.cpu_count(logical=False)) + "\n")
    res += ("Total cores:" +  str(ps.cpu_count(logical=True))+ "\n")
    # CPU frequencies
    cpufreq = ps.cpu_freq()
    res += (f"Max Frequency: {cpufreq.max:.2f}Mhz" + "\n")
    res += (f"Min Frequency: {cpufreq.min:.2f}Mhz"+ "\n")
    res += (f"Current Frequency: {cpufreq.current:.2f}Mhz" + "\n")
    # CPU usage
    res += ("CPU Usage Per Core: " + "\n")
    for i, percentage in enumerate(ps.cpu_percent(percpu=True, interval=1)):
        res += (f"Core {i}: {percentage}%" + "\n")
    res += (f"Total CPU Usage: {ps.cpu_percent()}% " + "\n")
    tb.reply_to(msg, res)
    mydb["cpuinfo"].insert_one({"LOG_TIME":str(date.today()),"cpuinfo":res})

@tb.message_handler(commands=['startlog'])
def startlog(msg):
    while True:
        get_CPU_Info(msg)
        get_Disk_Info(msg)
        get_IP_Info(msg)
        get_MEM_Info(msg)
        send_uptime(msg)
        time.sleep(60)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["isaa"]
tb.polling(none_stop=True, interval=3, timeout=20)


