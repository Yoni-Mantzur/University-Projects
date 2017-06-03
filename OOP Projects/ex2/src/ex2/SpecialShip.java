package ex2;

/**
 * Class that charge on Special ship -In start it looks like very easy pilot to kill but then it's attack
 * with all the power be ready!.
 * 
 * @see EnemyShip
 * @see SpaceShip
 * @author YONI
 *
 */
public class SpecialShip extends EnemyShip {

	private SpaceWars game;
	private int counterRoundes; 
	
	/**
	 * Constructor
	 */
	public SpecialShip() {
		
		counterRoundes = 0;
		
	}

    /**
     * Does the actions of this ship for this round. 
     * This is called once per round by the SpaceWars game driver.
     * 
     * @param game the game object to which this ship belongs.
     */
	@Override
	public void doAction(SpaceWars game) {
		
		this.game = game;

		this.counterRoundes++;
    	this.teleport();
    	this.specialBehavior(game);
    	this.fire(game);
    	this.setCurrentEnergy(Energy.CONSTANTLY_CHARGING);
	}
	
	
	/**
	 * Attempt to do a teleport. Just if it answer the precautions warning and 'life in danger'!
	 */
	@Override
	public void teleport(){
		
		if (isLifeInDanger() && this.getPrecautions.isAngelBreak(game, this))
			super.teleport();
	}
	
    /**
     * Attempts to fire a shot. Just if it answer the 'life in danger'!!
     * 
     * @param game the game object.
     */
	@Override
	public void fire(SpaceWars game){
		
		if (isLifeInDanger())
			super.fire(game);
	}

	/*
	 * Check if it's time to attack with all the massive power!
	 */
	private boolean isLifeInDanger(){
		
		if (this.getCurrentHealth() <= Precautions.LIFE_IN_DANGER)
			return true;
		return false;
		
	}
	
	/* The special behavior is to look a like a drunkard pilot until it's time to fight! */
	private void specialBehavior(SpaceWars game) {
				
		if (isLifeInDanger()){
			this.runAfterNearestShip(game);
		} else {
			if (this.counterRoundes % 15 == 0) // seems to look confused pilot
				this.getPhysics().move(ACCELERATION, TURN_LEFT);
			else
				this.getPhysics().move(ACCELERATION, TURN_RIGHT);
			
		}	
	}

}
