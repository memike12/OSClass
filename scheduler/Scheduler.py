from collections import deque
import copy

class Job:
    def __init__(self, id, arrivalTime, serviceTime1, priority):
        self.id = id
        self.priority = priority
        self.serviceTime = serviceTime1
        self.timeLeft = serviceTime1
        self.arrivalTime = arrivalTime
        self.started = False

    def starts(self, startTime):
        self.wait_time = int(startTime) - int(self.arrivalTime)
        self.startTime = startTime

    def startBool(self):
        self.started = False

    def swapBool(self):
        self.started = not self.started

    def complete(self, completionTime):
        self.completionTime = completionTime

    def decreaseTime(self, timeSlice):
        self.timeLeft = int(self.timeLeft) - int(timeSlice)

def FCFS( FCFSqueue):
    f = open('FCFScopy.txt', 'w')
    print('Starting FCFS')
    FCFScurrentJobs = deque([])
    time = 0
    Ready = True
    while len(FCFSqueue)>0 or len(FCFScurrentJobs)>0:
        if(len(FCFSqueue)>0 and int(time) == int(FCFSqueue[0].arrivalTime)):
            a = FCFSqueue.popleft()
            FCFScurrentJobs.append(a)
        if(len(FCFScurrentJobs)>0 and not Ready and time == FCFScurrentJobs[0].startTime + int(FCFScurrentJobs[0].serviceTime)):
            a = FCFScurrentJobs.popleft()
            a.complete(time)
            f.write(a.id + ' ' + str(a.arrivalTime) + ' ' + str(a.startTime) +' ' + str(a.completionTime) + '\n')
            Ready = True
        if(Ready and len(FCFScurrentJobs)>0): 
            FCFScurrentJobs[0].starts(time)
            Ready = False
        time = time + 1
    print('Finished FCFS')
    f.close()

def RoundRobin(RRqueue):
	file = open('RRcopy.txt', 'w')
	print('Starting Round Robin')
	RRcurrentJobs = deque([])
	time = 0
	runningTime = 0
	finished = False
	while len(RRqueue)>0 or len(RRcurrentJobs)>0:
		if(len(RRqueue)>0 and int(time) == int(RRqueue[0].arrivalTime)):
			RRcurrentJobs.append(RRqueue.popleft())
		if finished and len(RRcurrentJobs)>0:
			runningTime = 1
			finished = False
		if(len(RRcurrentJobs)>0):
			test = RRcurrentJobs[0].started
			if not test:
				RRcurrentJobs[0].starts(time)
				RRcurrentJobs[0].swapBool()
			x = RRcurrentJobs[0].timeLeft
			if(int(x) > 1):
				RRcurrentJobs[0].decreaseTime(1)
				if runningTime == 3:
					RRcurrentJobs.append(RRcurrentJobs.popleft()) 
					runningTime= 1 
					finished = True
			else:
				RRcurrentJobs[0].complete(int(time)+1)
				finished = True
				a = RRcurrentJobs[0]
				file.write(a.id + ' ' + str(a.arrivalTime) + ' ' + str(a.startTime) +' ' + str(a.completionTime) + '\n')
				RRcurrentJobs.popleft()
		time = time + 1
		runningTime = runningTime + 1
	print('Finished Round Robin')
	file.close()



def Priority(PriQueue):
	file = open('Pricopy.txt', 'w')
	print('Starting Priority')
	PriCurrentJobs = deque([])
	time = 0
	jobsSeen = 0
	jobsFinished = 0
	priorityLevelArray=[]
	done = False
	for x in range(11):	
		priorityLevelArray.append(deque([]))
	while len(PriQueue)>0 or not done:
		if( len(PriQueue) > 0 and int(time) == int(PriQueue[0].arrivalTime)):
			a = PriQueue[0]
			x = priorityLevelArray[int(a.priority)]
			x.append(PriQueue.popleft())
			jobsSeen = jobsSeen + 1
		for x in range(11):
			if len(priorityLevelArray[x]) > 0:
				done = False
				test = priorityLevelArray[x][0].started
				if not test:
					priorityLevelArray[x][0].starts(time)
					priorityLevelArray[x][0].swapBool()
				if int(priorityLevelArray[x][0].timeLeft) > 1:
					priorityLevelArray[x][0].decreaseTime(1)
					break
				else:
					priorityLevelArray[x][0].complete(time+1)
					file.write(priorityLevelArray[x][0].id + ' ' + str(priorityLevelArray[x][0].arrivalTime) \
								+ ' ' + str(priorityLevelArray[x][0].startTime) + ' ' \
								+ str(priorityLevelArray[x][0].completionTime) + '\n')
					priorityLevelArray[x].popleft()
					jobsFinished = jobsFinished + 1
					break
			if jobsSeen == jobsFinished:
				done = True
			else:
				done = False
		time = time + 1
	print('Finished Priority')
	file.close()



def SPN(SPNQueue):
	file = open('SPNcopy.txt', 'w')
	print('Starting SPN')
	time = 0
	jobsSeen = 0
	jobsFinished = 0
	SPNLevelArray=[]
	runningAt = 0
	done = False
	blocked = False
	for x in range(11):	
		SPNLevelArray.append(deque([]))
	while len(SPNQueue)>0 or not done:
		if( len(SPNQueue) > 0 and int(time) == int(SPNQueue[0].arrivalTime)):
			a = SPNQueue[0]
			SPNLevelArray[int(a.serviceTime)].append(SPNQueue.popleft())
			jobsSeen = jobsSeen + 1
		if blocked:
			if int(SPNLevelArray[runningAt][0].timeLeft) > 1:
				SPNLevelArray[runningAt][0].decreaseTime(1)
			else:
				SPNLevelArray[runningAt][0].complete(time+int(SPNLevelArray[runningAt][0].timeLeft)-1)
				file.write(SPNLevelArray[runningAt][0].id + ' ' \
							+ str(SPNLevelArray[runningAt][0].arrivalTime)  \
							+ ' ' + str(SPNLevelArray[runningAt][0].startTime) \
							+ ' ' + str(SPNLevelArray[runningAt][0].completionTime) + '\n')
				SPNLevelArray[runningAt].popleft()
				jobsFinished = jobsFinished + 1
				blocked = False
		if not blocked:
			for x in range(11):
				if len(SPNLevelArray[x]) > 0:
					done = False
					SPNLevelArray[x][0].starts(time)
					SPNLevelArray[x][0].startBool()
					blocked = True
					runningAt = x
					break
		if jobsSeen == jobsFinished:
			done = True
		else:
			done = False
		time = time + 1
	print('Finished SPN')
	file.close()



def SRT(SRTQueue):
	file = open('SRT.txt', 'w')
	print('Starting SRT')
	SRTCurrentJobs = deque([])
	time = 0
	jobsSeen = 0
	jobsFinished = 0
	SRTLevelArray=[]
	done = False
	for x in range(11):	
		SRTLevelArray.append(deque([]))
	while len(SRTQueue)>0 or not done:	
		if( len(SRTQueue) > 0 and int(time) == int(SRTQueue[0].arrivalTime)):
			a = SRTQueue[0]
			a.timeLeft = a.serviceTime 
			SRTLevelArray[int(a.serviceTime)].append(SRTQueue.popleft())
			jobsSeen = jobsSeen + 1
	
		for x in range(11):
			if len(SRTLevelArray[x]) > 0:
				done = False
				if int(SRTLevelArray[x][0].timeLeft) > 1:
					SRTLevelArray[x][0].decreaseTime(1)
					a = SRTLevelArray[x].popleft()				
					test = a.started
					if(not test):
						a.starts(time)
						a.swapBool()
					SRTLevelArray[a.timeLeft].append(a)
					break
				else:
					#if(int(SRTLevelArray[x][0].timeLeft) < 2):
					SRTLevelArray[x][0].complete(time+1)
					test = SRTLevelArray[x][0].started
					if(not test):
						SRTLevelArray[x][0].starts(time)
						SRTLevelArray[x][0].swapBool()
					file.write(SRTLevelArray[x][0].id + ' ' + str(SRTLevelArray[x][0].arrivalTime) \
								+ ' ' + str(SRTLevelArray[x][0].startTime) +' ' \
								+ str(SRTLevelArray[x][0].completionTime) + '\n')
					SRTLevelArray[x].popleft()
					jobsFinished = jobsFinished + 1
					break
			if jobsSeen == jobsFinished:
				done = True
			else:
				done = False
		time = time + 1
	print('Finished SRT')
	file.close()

def HRRN(HRRNQueue):
	file = open('HRRNcopy.txt', 'w')
	print('Starting HRRN')
	HRRNCurrentJobs = deque([])
	time = 0
	jobsSeen = 0
	jobsFinished = 0
	done = False
	blocked = False
	minIndex = 0
	while len(HRRNQueue)>0 or not done:	
		if len(HRRNQueue) > 0 and int(time) == int(HRRNQueue[0].arrivalTime):
			a = HRRNQueue[0]
			HRRNCurrentJobs.append(HRRNQueue.popleft())
			jobsSeen = jobsSeen + 1
		if len(HRRNCurrentJobs) > 0 and not blocked:
			done = False
			min = (time - int(HRRNCurrentJobs[0].arrivalTime) + int(HRRNCurrentJobs[0].timeLeft))/int(HRRNCurrentJobs[0].serviceTime)
			for x in range(len(HRRNCurrentJobs)):
				tempMin = (time - int(HRRNCurrentJobs[x].arrivalTime) + int(HRRNCurrentJobs[x].timeLeft))/int(HRRNCurrentJobs[x].serviceTime)
				if tempMin > min:
					minIndex = x
			HRRNCurrentJobs[minIndex].starts(time)
			blocked = True
		if len(HRRNCurrentJobs) > 0:		
			if int(HRRNCurrentJobs[minIndex].timeLeft) > 1:
				HRRNCurrentJobs[minIndex].decreaseTime(1)
			else:
				HRRNCurrentJobs[minIndex].complete(time+1)
				a = HRRNCurrentJobs[minIndex]
				HRRNCurrentJobs.remove(a)
				file.write(a.id + ' ' + str(a.arrivalTime) + ' ' + str(a.startTime) +' ' + str(a.completionTime) + '\n')
				jobsFinished = jobsFinished + 1
				blocked=False
				minIndex = 0
			if jobsSeen == jobsFinished:
				done = True
			else:
				done = False
		time = time + 1
	print('Finished HRRN')
	file.close()

def printValues(algs):
	progOutput = open('output.txt', 'w')
	for alg in algs:
		filename = alg + '.txt'
		file = open(filename, 'r')
		avgThru = 0
		avgRT = 0
		avgTAT = 0
		finishTime = 0
		for line in file:
			arriveTime = line.split(' ')[1].strip()
			startTime = line.split(' ')[2].strip()
			finishTime = line.split(' ')[3].strip()
			avgRT = avgRT + int(startTime) - int(arriveTime)
			avgTAT = avgTAT + int(finishTime) - int(arriveTime)
		avgTAT = avgTAT/jobTotal
		avgRT = avgRT/jobTotal
		avgThru = int(finishTime)/jobTotal
		progOutput.write('Algorithm: ' + alg + '\t  Turn Around Time: ' + str(avgTAT) + '\t Response Time: ' + str(avgRT)  + ' \t Through Put: ' + str(avgThru) + '\n')
		file.close()
	progOutput.write('The worst algorithm based on fairness would have to be Priority scheduling. If just a task with a lower priority comes along, and there are a bunch of high priority tasks, the low priority task could easily die due to starvation.\n')

f = open('jobdata.txt', 'r')
FCFSqueue = deque([])
RRqueue = deque([])
Priorityqueue = deque([])
SPNQueue = deque([])
SRTQueue = deque([])
HRRNQueue = deque([])
jobList = []
jobTotal = 0
for line in f:
	job = Job(line.split(' ')[0], line.split(' ')[1], line.split(' ')[2], line.split(' ')[4].strip())
	jobTotal = jobTotal + 1
	jobList.append(job)
	FCFSqueue.append(job)
	RRqueue.append(job)
	Priorityqueue.append(job)
	SPNQueue.append(job)
	SRTQueue.append(job)
	HRRNQueue.append(job)
f.close()

#FCFS(FCFSqueue)
#RoundRobin(RRqueue)
#Priority(Priorityqueue)
#SPN(SPNQueue)
#SRT(SRTQueue)
#HRRN(HRRNQueue)

algs = ['FCFS', 'RR', 'Pri', 'SPN', 'SRT', 'HRRN']

printValues(algs)

















