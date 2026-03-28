from time import time

class Timer:
    #__init__(self, parent, time_limit, timer_active):
    #Sets up the Timer object. parent is the object that created the Timer, in this case a LevelHandler object.
    #time_limit is the overall time left when the timer is started/resumed.
    #timer_active is a Boolean that says if the timer is currently counting down.
    def __init__(self, parent, time_limit: int, timer_active: bool):
        self.__parent = parent
        self.__time_limit = time_limit
        self.__time_remaining = time_limit #time remaining starts at time limit and then decreases.
        self.__timer_active = timer_active

        self.__time_started = time() #stores the time that the timer is started to calculate time remaining.
    
    def __update_times(self) -> None:
        if self.__timer_active == True: #only updates if timer active.
            if self.__time_remaining > 0:
                self.__time_remaining = self.__time_limit - int(time()-self.__time_started) #subtracts time passed (current time - time started) from time limit.
            else:
                self.__time_remaining = 0 #if time remaining under 0, set it to 0.
    
    def get_minute_second_time_left(self) -> tuple: #returns time remaining in minutes and seconds.
        self.__update_times() #update times first to return accurate time remaining.
        minutes = int(self.__time_remaining//60)
        seconds = int(self.__time_remaining%60)

        return (minutes, seconds)
    
    def pause_timer(self): #deactivates timer if active. Updates times first so that current state of paused timer will be accurate.
        if self.__timer_active == True:
            self.__update_times()
            self.__timer_active = False
    
    def resume_timer(self): #if timer deactivated, reactivates it.
        if self.__timer_active == False:
            self.__time_limit = self.__time_remaining #sets the time limit to the time remaining and records the current time. Basically creates a shorter timer.
            self.__time_started = time()
            self.__timer_active = True
    
    def check_finished(self): #returns whether time remaining is 0. updates times first to ensure accurate result.
        self.__update_times()
        return self.__time_remaining == 0