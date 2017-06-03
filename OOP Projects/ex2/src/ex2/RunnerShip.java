package ex2;

/**
 * Class that charge on Runner ship - always trying to avoid facing fight.
 * 
 * @see EnemyShip
 * @see SpaceShip
 * @author YONI
 *
 */
public class RunnerShip extends EnemyShip{
	

	private SpaceWars game;
	
	/**
	 * Constructor
	 */
	public RunnerShip() {
		
	}

    /**
     * Does the actions of this ship for this round. 
     * This is called once per round by the SpaceWars game driver.
     * 
     * @param game the game object to which this ship belongs.
     */
	public void doAction(SpaceWars game) {

		this.game = game;
		
    	this.teleport();
    	this.specialBehavior(game);
    	this.setCurrentEnergy(Energy.CONSTANTLY_CHARGING);
	}
	
	/**
	 * Attempt to do a teleport. Just if it answer the precautions warning!
	 */
	@Override
	public void teleport(){

		if (this.getPrecautions.isAngelBreak(this.game, this) && 
				(this.getPrecautions.isDistanceBreak(this.game, this)))
			super.teleport();	
	}
	
	
	/* The special behavior is to run from fight all the time! */
	private void specialBehavior(SpaceWars game) {
				
		// do the next move
		SpaceShip nearestShip = game.getClosestShipTo(this);
		
		// If the angle is positive goes the opposite way!
		if (this.getPhysics().angleTo(nearestShip.getPhysics()) > 0) 
			this.getPhysics().move(ACCELERATION, TURN_RIGHT);
		else
			this.getPhysics().move(ACCELERATION, TURN_LEFT);
		
	}



}
