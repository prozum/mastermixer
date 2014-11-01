from sqlite3 import dbapi2 as sqlite3
from libliquor import Actuator,Ranger,Mixer

config = dict(
    DEBUG=True,
    DATABASE='/tmp/flaskr.db',
)

# Setup objects
if not config["DEBUG"]:
    motor   = Actuator(10)
    piston  = Actuator(11)
    valves  = [Actuator(12), Actuator(13)]
    rangers = [Ranger(0), Ranger(1)]
    mixer   = Mixer(motor,piston,valves,rangers)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    return connect_db()

def make_recipe():
    db = get_db()
    order,product = db.execute('SELECT Id, P_Id FROM Orders ORDER BY Id ASC LIMIT 1').fetchone() # Get order and product
    
    db.execute('DELETE FROM Orders WHERE Id ='+str(order)) # Delete order
    db.commit()
    
    data = list(db.execute('SELECT Stat1, Stat2, Stat3 FROM Products Where Id ='+str(product)).fetchone()) # Get drink data
    
    load = data[0]/100.0
    data = data[1:]
    
    rations = 0
    for i in range(len(data)):
        rations+=data[i]
    
    recipe = []
    for i in range(len(data)):
        recipe.append(data[i]/float(rations)*load)
    
    return recipe

def show_recipe(recipe,max=250):
    print(recipe)
    for i in range(len(recipe)):
        print("liquid "+str(i)+":"+str(recipe[i]*max))
    

def main():
    while 1:
        recipe = make_recipe()
        if config["DEBUG"]:
            show_recipe(recipe)
            break
        mixer.mix_drink(recipe)
        mixer.serve()
        time.sleep(10)

if __name__ == "__main__":
    main()