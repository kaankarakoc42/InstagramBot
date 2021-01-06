from main import InstaBot

bot=InstaBot()
bot.login("username","password")

#bot.getFollows() #takip ettiklerinin listesini verir.
#bot.getFollowers() # takipçilerin listesini verir.
#bot.followAllFollowers() #seni takip eden herkesi geri takip et.
#bot.removeUnFollowers()  #seni geri takip etmeyen herkesi takipten çıkar.
#bot.update() #detaylı bilgi döndürür

bot.stop()




 

