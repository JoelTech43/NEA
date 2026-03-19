from time import time

class Timer:
    def __init__(self, parent, time_limit: int, timer_active: bool):
        self.__parent = parent
        self.__time_limit = time_limit
        self.__time_remaining = time_limit
        self.__timer_active = timer_active

        self.__time_started = time()
    
    def __update_times(self) -> None:
        if self.__timer_active == True:
            if self.__time_remaining > 0:
                self.__time_remaining = self.__time_limit - int(time()-self.__time_started)
            else:
                self.__time_remaining = 0
    
    def get_minute_second_time_left(self) -> tuple:
        self.__update_times()
        minutes = int(self.__time_remaining//60)
        seconds = int(self.__time_remaining%60)

        return (minutes, seconds)
    
    def pause_timer(self):
        if self.__timer_active == True:
            self.__update_times()
            self.__timer_active = False
    
    def resume_timer(self):
        if self.__timer_active == False:
            self.__time_limit = self.__time_remaining
            self.__time_started = time()
            self.__timer_active = True
    
    def check_finished(self):
        self.__update_times()
        return self.__time_remaining == 0