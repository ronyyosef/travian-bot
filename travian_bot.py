import constant
import travian_bot_F


#################################################
#   here you can build your task bot the bot    #
#################################################
###################exsmple#######################
def control_game(bot, capital):
    while True:
        bot.hero_adventure()                               #send your hero to an adventure
        bot.build_task_main_city(constant.Main_Building,5) #build main building to lvl 5
        bot.build_task_resorurce_all_to_lvl(5)             #build all your resource to lvl 5
        bot.train_troop(wood=100, clay=100, iron=100, lumber=100)#train max troop if you have more then 100 for each resoruce
        bot.switch_to_next_city()                          #swith to the next city


if __name__ == '__main__':
    bot = travian_bot_F.Bot('URL OF THE SERVER', 'USERNAME', 'PASSWORD')
    bot.login()
    control_game(bot, bot.get_capital())
    bot.close_browser()
