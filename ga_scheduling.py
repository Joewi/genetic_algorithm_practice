from statistics import *
from numpy import *
from random import *
from operator import itemgetter

# 0 日班
# 1 夜班
# 2 大夜班
# 3 放假

CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.1
ITERATION_TIME = 20     #迭代次數
NUMBER_OF_GENETIC = 10   #基因數量
NUMBER_OF_WORKER = 18    #工作人數


# 染色體集合
all_genetic = []
best_genetic = []
best_genetic_target_value = 1000000000000

def targetFunction(teamSchedule, showValue=False):
  # O -> 休假次數
  # µ0 -> 平均休假次數
  # 變異數
  day_shift = [] #日班
  later_shift = []
  grave_shift = []
  for i in range(NUMBER_OF_WORKER):
    # 日班
    day_shift.append(len([i for i in teamSchedule[i] if i == 0]))
    # 夜班
    later_shift.append(len([i for i in teamSchedule[i] if i == 1]))
    # 大夜班
    grave_shift.append(len([i for i in teamSchedule[i] if i == 2]))

  target_value = round(variance(day_shift)+variance(later_shift)+variance(grave_shift), 10)
  if showValue:
    print('Total variance: ', target_value )
  return target_value


def crossover(): # 單點交配
  crossover_if = random()
  if( crossover_if > CROSSOVER_RATE): # 判斷是否要交配
    print('不交配')
    return
  else:
    # 隨機取兩個個體
    first = int(random() * (NUMBER_OF_GENETIC))-1
    second = int(random() * (NUMBER_OF_GENETIC))-1
    while(first==second):
      second = int(random() * (NUMBER_OF_GENETIC))-1
    crossover_genetic_1 = all_genetic[first]
    crossover_genetic_2 = all_genetic[second]

    # 取得突變位置
    crossover_worker = int(random() * (NUMBER_OF_WORKER-1) ) # 取第幾個工人
    crossover_date = int(random() * (28-1) ) # 取工人第幾天的工作

    for i in range(crossover_date):
      temp = crossover_genetic_1[crossover_worker][i]
      crossover_genetic_1[crossover_worker][i] = crossover_genetic_2[crossover_worker][i]
      crossover_genetic_2[crossover_worker][i] = temp
    print('交配')
  return

# 每個染色體隨意找地方把一個值改成另一個
def muation():
  global all_genetic
  # muation_if = random()
  # if( muation_if > MUTATION_RATE): # 判斷是否要突變
  #   print('不突變')
  #   return
  # else:

  genetic_mutation = int(random() * (NUMBER_OF_GENETIC-1))
  worker_mutation = int(random() * (NUMBER_OF_WORKER-1))

  new_genetic = generateEachWorker()[:]
  all_genetic[genetic_mutation][worker_mutation] = new_genetic[:]
  print('突變')
  return

def generateEachWorker():
  each_worker = []

  workDay = 0
  holiday = 0 #放假數量
  vacation = 0 #休假數量
  for i in range(4):
    for j in range(7):
      if(holiday>=2):
        work_type = int(random() * 3)
      else:
        work_type = int(random() * 4)
        if(work_type==3):
          holiday+=1
        else:
          workDay+=1
      each_worker.append(work_type)

    holiday=0
  return each_worker

def initializeGenetic():
  for i in range(NUMBER_OF_GENETIC):
    one_genetic = []
    for j in range(NUMBER_OF_WORKER):
      one_genetic.append(generateEachWorker()[:])
    all_genetic.append( one_genetic[:] )
    
    # 記錄最好的基因
    if(i == 0):
      best_genetic = one_genetic[:]
      best_genetic_target_value = targetFunction(best_genetic)
    elif(best_genetic_target_value > targetFunction(one_genetic) ):
      best_genetic = one_genetic[:]
      best_genetic_target_value = targetFunction(best_genetic)

def selectNextGeneration(number_of_generation):
  global all_genetic
  global best_genetic_target_value
  temp_all_genetic = []
  biggestTargetValue = -1
  population = []

  for j in range(NUMBER_OF_GENETIC):
    targetValue = targetFunction(all_genetic[j])
    population.append(targetValue)
    if(biggestTargetValue < targetValue):
      biggestTargetValue = targetValue

  # 如果全部基因都一樣沒有交配或突變就不用演進了
  different = True
  for i in range(1,len(population)):
    d = population[0]
    if(d!=population[i]):
      different = False

  if different:
    return

  for i in range(len(population)):
    population[i] = biggestTargetValue - population[i]

  for i in range(NUMBER_OF_GENETIC):
    x = choices( range(len(population)), population )
    temp_all_genetic.append(all_genetic[x[0]][:] )
  all_genetic = temp_all_genetic[:]

  print('\n','============= ITERATION ', number_of_generation ,' =============')
  for i in range(NUMBER_OF_GENETIC): # 印出genetic 變異數
    targetValue = targetFunction(all_genetic[i], True)

    # 記錄最好的基因
    if(best_genetic_target_value > targetFunction(all_genetic[i]) ):
      best_genetic = all_genetic[i]
      best_genetic_target_value = targetFunction(best_genetic)
  print('Best Genetic Target Value: ', best_genetic_target_value)
  return

def main():
  initializeGenetic() # 初始化: 建立所有基因
  # 可以設定進步幅度不大的話就停下來，例如：在20代中，無法進步1%就停下來
  for i in range(ITERATION_TIME):
    selectNextGeneration(i+1) # 選擇: 選擇下一代基因
    crossover() # 交配
    muation() # 突變 => 突變一點太小了，這邊直接突變一個工人的全部
    muation() # 

if __name__ == "__main__":
    main()