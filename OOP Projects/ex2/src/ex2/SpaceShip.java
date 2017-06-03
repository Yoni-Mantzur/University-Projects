package ex2;
import oop.ex2.*;

import java.awt.Image;

/**
 * Class represent the abstract SpaceShip in the game.
 * Each ship subclass of this class is an object will be part of the game.
 * @see Energy
 * @see Health
 * @see Shootable
 *  
 * @author Oop staff and Yoni Mantzur
 */
public abstract class SpaceShip implements Energy, Health, Shootable{
	
	/**  The SHIP can move as decided to, right turn means -1. */
	public static final int TURN_RIGHT = -1;
	/**  The human player can move as decided to, left turn means 1. */
	public static final int TURN_LEFT = 1;
	/**  The human player can move as decided to, no turn means 0. */
	public static final int NO_TURN = 0;
	

	// Composition - shield - the shield of a ship can put on. 
	private Shield shield;
	// Composition - shipPhysics - the status of a ship in the game.
	private SpaceShipPhysics shipPhysics;
	// Fields that every ship will have
	private int maxEnergyLevel;
	private int currentEnergy;
	private int healthLevel;
	private int counterRoundsToShot;

	
	/**
	 * Constructor.
	 */
	public SpaceShip(){
		
		this.shipPhysics = new SpaceShipPhysics();
		this.maxEnergyLevel = Energy.START_ENERGY;
		this.currentEnergy = Energy.START_ENERGY;
		this.healthLevel = Health.START_HEALTH;
		this.shield = new Shield();
		this.counterRoundsToShot = LIMIT_SHOOT_PER_ROUNDS;
	}

   
    /**
     * Does the actions of this ship for this round. 
     * This is called once per round by the SpaceWars game driver.
     * 
     * @param game the game object to which this ship belongs.
     */
    public abstract void doAction(SpaceWars game);
    
 
    /**
     * This method is called every time a collision with this ship occurs 
     * Bashing - is when ship has been collided with other ship and the shields was on
     */
    public void collidedWithAnotherShip(){
    	
    	if (!this.shield.isSheildActivated()){

    		// The deduction in the energy
    		this.setCurrentEnergy(Energy.GOT_HITTING_IMPACT);
    		this.setCurrentHealth(Health.GOT_HITTING_IMPACT);
    		
    	} else {
    		// The improvement in the energy
    		this.setMaxEnergy(Energy.BASHING_IMPACT);
    		this.setCurrentEnergy(Energy.BASHING_IMPACT);
    	}
    	
    }

    /** 
     * This method is called whenever a ship has died. It resets the ship's 
     * attributes, and starts it at a new random position.
     */
    public void reset(){
    	
    	// Initialize all the relevant arguments
		this.shipPhysics = new SpaceShipPhysics();
		this.maxEnergyLevel = Energy.START_ENERGY;
		this.currentEnergy = Energy.START_ENERGY;
		this.healthLevel = Health.START_HEALTH;
		this.shield.turnOff();
		this.counterRoundsToShot = LIMIT_SHOOT_PER_ROUNDS;
    }

    /**
     * Checks if this ship is dead.
     * 
     * @return true if the ship is dead. false otherwise.
     */
    public boolean isDead() {
        if (this.healthLevel > Health.MINIMAL_HEALTH)
        	return false;
        return true;
    }

    /**
     * Gets the physics object that controls this ship.
     * 
     * @return the physics object that controls the ship.
     */
    public SpaceShipPhysics getPhysics() {
        return this.shipPhysics;
    }
    
    /**
     * This method is called by the SpaceWars game object when ever this ship
     * gets hit by a shot.
     */
    public void gotHit() {
    	
    	if (!this.shield.isSheildActivated()){
    		
    		this.setCurrentEnergy(Energy.GOT_HITTING_IMPACT);
    		this.setCurrentHealth(Health.GOT_HITTING_IMPACT);
    	}
    }
    
	/**
	 * Get the current energy of this object. Implement of Energy interface.
	 * @return the current energy
	 */
	public int getCurrentEnergy() {
		
		return this.currentEnergy;
	}

	/**
	 * Set new current energy. Implement of Energy interface.
	 * @param addFactor - additional value for the current energy.
	 */
	public void setCurrentEnergy(int addFactor) {
		this.currentEnergy += addFactor;
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		// Check that not go over the max value
		if (this.currentEnergy > this.maxEnergyLevel)
			this.currentEnergy = this.maxEnergyLevel;
		
		else if (this.currentEnergy < Energy.MINIMAL_ENERGY)
			this.currentEnergy = Energy.MINIMAL_ENERGY;
		
	}

	/**
	 * Get the max energy of this object. Implement of Energy interface.
	 * @return the max energy
	 */
	public int getMaxEnergy() {

		return this.maxEnergyLevel;
	}

	/**
	 * Set new max energy. Implement of Energy interface.
	 * @param addFactor - additional value for the max energy.
	 */
	public void setMaxEnergy(int addFactor) {
		this.maxEnergyLevel += addFactor;
		
		if (this.maxEnergyLevel < Energy.MINIMAL_ENERGY)
			this.maxEnergyLevel = Energy.MINIMAL_ENERGY;
		
	}

	/**
	 * Get the current Health points of this object. Implement of Health interface.
	 * @return the current energy
	 */
	public int getCurrentHealth() {

		return this.healthLevel;
	}


	/**
	 * Set new current Health points. Implement of Health interface.
	 * @param addFactor - additional value for the current energy.
	 */
	public void setCurrentHealth(int addFactor) {

		this.healthLevel += addFactor;
		
		if (this.healthLevel < Health.MINIMAL_HEALTH)
			this.healthLevel = Health.MINIMAL_HEALTH;
		
	}

    /**
     * Gets the image of this ship. This method should return the image of the
     * ship with or without the shield. This will be displayed on the GUI at
     * the end of the round.
     * 
     * @return the image of this ship.
     */
    public abstract Image getImage();
    
	/**
	 * Function that check if it can be a attempt of shooting. 
	 * @return true if so or false if not passed 8 rounds or there is no energy
	 */  
    public boolean isFiredAvailable(){
    	
    	if (counterRoundsToShot < Shootable.LIMIT_SHOOT_PER_ROUNDS){
    		this.counterRoundsToShot++;
    		return false;
    	}
    	
    	return true;
    }
    
    /**
     * Attempts to fire a shot.
     *@param game the game object.
     */
    public void fire(SpaceWars game){
    	
		if ((this.getCurrentEnergy() >= -Energy.FIRRING_IMPACT) && this.isFiredAvailable()){
		
			game.addShot(this.getPhysics());
			counterRoundsToShot = 0;
			this.setCurrentEnergy(Energy.FIRRING_IMPACT);
		}
    }
    
       
	/**
	 * Get the shield of this ship.
	 * @return the shield of the ship
	 */
    public Shield getShield(){
    	
    	return this.shield;
    }
    
    /**
     * Attempts to turn on the shield.
     */
    public void shieldOn(){
    	
		if (this.getCurrentEnergy() >= -Energy.SHIELD_USE)	{
			
			this.shield.activeSheild();
			this.setCurrentEnergy(Energy.SHIELD_USE);
		} else {
			this.shield.turnOff();
			
		}
    }
		

    /**
     * Attempts to teleport.
     */
    public void teleport(){
    	
		if (this.getCurrentEnergy() >= -Energy.TARNSPOSED_IMPACT){
			
			this.shipPhysics = new SpaceShipPhysics();
			this.setCurrentEnergy(Energy.TARNSPOSED_IMPACT);
		}
    }
    
}
