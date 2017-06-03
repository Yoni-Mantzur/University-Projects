package ex2;

/**
 * A factory for creating instances of spaceShipe regard to chosen of the input in line command.
 * @author YONI
 */
public class SpaceShipFactory {
	
	/** Each letter represent a kind of ship will be in the game. */
	/** Human ship*/
	public static final String HUMAN = "h";
	/** Runner ship*/
	public static final String RUNNER = "r";
	/** Basher ship */
	public static final String BASHER = "b";
	/** Aggressive ship*/
	public static final String AGGRESSIVE = "a";
	/** Drunken ship*/
	public static final String DRUNKARD = "d";
	/** Special ship */
	public static final String SPECIAL = "s";
	
	/**
	 * Static method return instances of spaceShipe regard the arguments were inputed. 
	 * @param args - array of strings represent the kinds of spaceShips
	 * @return arraySpaceShips - array of instances of spaceShip
	 */
    public static SpaceShip[] createSpaceShips(String[] args) {
      
        SpaceShip[] arraySpaceShips = new SpaceShip[args.length]; // using polymorphism!

        for (int i=0; i<arraySpaceShips.length; i++){
        	
        	switch(args[i]){
        	
        		case HUMAN:
        			arraySpaceShips[i] = new HumanControlledShip();
        			break;
        		case RUNNER:
        			arraySpaceShips[i] = new RunnerShip();
        			break;
        		case BASHER:
        			arraySpaceShips[i] = new BasherShip();
        			break;
        		case AGGRESSIVE:
        			arraySpaceShips[i] = new AggressiveShip();
        			break;
        		case DRUNKARD:
        			arraySpaceShips[i] = new DrunkaedShip();
        			break;
        		case SPECIAL:
        			arraySpaceShips[i] = new SpecialShip();
        			break;
        			
        		default: // non value input
        			return null;
        			
        	}	
        }
        	
        return arraySpaceShips;
    }
}
