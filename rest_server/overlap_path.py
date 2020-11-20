import requests
import json
import math

# x-> latitude, y -> longitude
def trim_list(x_1,y_1,x_2,y_2) :

    min_len = min(len(x_1),len(y_1),len(x_2),len(y_2))

    a = min_len % 5

    return (x_1[:min_len-a], y_1[:min_len-a], x_2[:min_len-a], y_2[:min_len-a])

def scoring_system(x_1,y_1,x_2,y_2) : #(1m, 15min) : 100 point, (2m, 5min) : 50point

    avg_distance_list = []
    i = 0
    list_len = len(x_1) # same with total estimated minutes

    while(i <= list_len-15) :
        sum = 0
        for j in range(15):
            sum = sum + math.sqrt( (6400*2*3.14/360*(x_1[i+j] - x_2[i+j])) ** 2 + 
            (math.cos(math.pi/180*x_1[i+j])*6400*2*3.14/360*(y_1[i+j] - y_2[i+j])) ** 2) # (latitude, longitude -> km) 
        
        #print(sum)
        avg_distance_list.append(sum/15*1000) #m
        
        i= i + 5

    avg_distance_list.sort()
    
    return 100 - 0.495 * avg_distance_list[0] # when min distance, score

def covid_user_route() :
    response = requests.get("http://192.249.19.250:7880/api/v1/route/allCovidUsers")
    covid_user_route = response.json()
    i = 0
    x_1=[]
    y_1=[]
    while(i < len(covid_user_route)) :
        x_1.append(covid_user_route[i]['latitude']) # 우선 한 사람만 있으므로 sample code
        y_1.append(covid_user_route[i]['longitude'])
        i = i+1
    
    

    return (x_1,y_1)

def notify_score_each_no_covid_user(x_1,y_1) :

    i = 0
    response = requests.get("http://192.249.19.250:7880/api/v1/user")
    user = response.json()
    no_covid_user = []
    while (i<len(user)) :
        if ( user[i]['isCOVID'] == False ) :
            no_covid_user.append(user[i])
        i = i + 1


    # send message each no-covid-user 
    j = 0
    while (j<len(no_covid_user)) :
        response = requests.get("http://192.249.19.250:7880/api/v1/route/user/?userID=%d" %no_covid_user[j]['id'])
        user_route = response.json()
        k = 0
        x_2=[]
        y_2=[]
        while(k < len(user_route)) :
            x_2.append(user_route[k]['latitude']) # 우선 한 사람만 있으므로 sample code
            y_2.append(user_route[k]['longitude'])
            k = k+1
        
        #print(x_2,y_2)
        j= j+1
        
        (x_1,y_1,x_2,y_2) = trim_list(x_1,y_1,x_2,y_2)
        
        score = scoring_system(x_1,y_1,x_2,y_2) # position per minutes and its length should be multiple of 5
        print(score)
        if (score >= 50) :
            print("your score is %d, you should check whether you get covid or not" %score ) # 카톡 메시지로 보낼 내용 
        


if __name__ == '__main__':
    '''
    x_1 = [100,100,100,100,100,100,100,100,100,100,00,00,00,00,100,100,100,100,100,100,100,100,100,100,100,100,100,100]
    y_1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    x_2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    y_2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    '''
    
    (x_1,y_1) = covid_user_route()

    #print(x_1,y_1)

    notify_score_each_no_covid_user(x_1,y_1)