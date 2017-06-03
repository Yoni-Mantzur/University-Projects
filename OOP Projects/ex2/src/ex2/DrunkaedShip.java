package ex2;

import java.util.Random;

/**
 * The Class represent an Drunkard ship, flying like there is a drunkard pilot in it and randomly 
 * shoot or teleport.
 * 
 * @see EnemyShip
 * @see SpaceShip
 * @author YONI
 *
 */
public class DrunkaedShip extends EnemyShip {
	
	private Random randomFire;
	private boolean noFire;
	

	/**
	 * Constructor
	 */
	public DrunkaedShip() {
		
		super();
		randomFire = new Random();
		noFire = true;	
	}

    /**
     * Does the actions of this ship for this round. The ship trying to do nothing but as you can see
     * it really hard to destroyed it! teleport and fire randomly.  
     * This is called once per round by the SpaceWars game driver.
     * 
     * @param game the game object to which this ship belongs.
     */
	@Override
	public void doAction(SpaceWars game) {

			this.teleport();
			this.specialBehavior(game);
			this.fire(game);
			this.setCurrentEnergy(Energy.CONSTANTLY_CHARGING);

	}
	
    /**
     * Attempts to fire a shot when ever the pilot feels he wants to break something :)
     * 
     * @param game the game object.
     */
	public void fire(SpaceWars game){
		
		if (randomFire.nextInt(5) == 1){ // Chosen randomly numbers
			noFire = false;
			super.fire(game);
		} else {
		
			noFire = true;
		}
		
	}
	
	/**
	 * Attempt to do a teleport when he can't fire!
	 */
	@Override
	public void teleport(){
		
		if (!noFire)
			super.teleport();
	}
	
	/* It's special behavior is to fly in circle exactly likes how you go when you drunk! */
	private void specialBehavior(SpaceWars game){
		
			this.getPhysics().move(ACCELERATION, TURN_LEFT);
	}

}
