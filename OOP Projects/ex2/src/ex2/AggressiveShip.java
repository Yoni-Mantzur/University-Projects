package ex2;


/**
 * The Class represent an Aggressive ship, trying to fly after the nearest ship and if 
 * it answer the precautions warning it will fire!
 * 
 * @see EnemyShip
 * @see SpaceShip
 * @author YONI
 *
 */
public class AggressiveShip extends EnemyShip {


	/**
	 * Constructor
	 */
	public AggressiveShip() { // I know this is no must code, but prefer to know the super constructor is called	
		super();
	}

    /**
     * Does the actions of this ship for this round. The ship trying to run after the nearest ship and fire
     * at it when it's very close.  
     * This is called once per round by the SpaceWars game driver.
     * 
     * @param game the game object to which this ship belongs.
     */
	@Override
	public void doAction(SpaceWars game) {
		
		this.specialBehavior(game);
		this.fire(game);
		this.setCurrentEnergy(Energy.CONSTANTLY_CHARGING);

	}
	
    /**
     * Attempts to fire a shot. Just if it answer the precautions warning!
     * 
     * @param game the game object.
     */
	@Override
    public void fire(SpaceWars game){
		
		if (this.getPrecautions.isAngelBreak(game, this))
			super.fire(game);
	}
	
	/* The special behavior is to run after the closest ship */
	private void specialBehavior(SpaceWars game){
			
		this.runAfterNearestShip(game);
		
	}

}
