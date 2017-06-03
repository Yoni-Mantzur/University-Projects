package ex2;

import java.awt.Image;

import oop.ex2.*;

/**
 * Class charge on HumanControlled ship, the pilot can to what ever he likes to!
 * 
 * @see SpaceShip
 * @author YONI
 *
 */
public class HumanControlledShip extends SpaceShip{
	
	private Image currentImageShip; // with or without shield
	private SpaceWars game;
	
	/**
	 * Constructor.
	 */
	public HumanControlledShip(){
		
		super();
		this.currentImageShip = GameGUI.SPACESHIP_IMAGE;
		
	}
	
    /**
     * Does the actions of this ship for this round. 
     * This is called once per round by the SpaceWars game driver.
     * 
     * @param game the game object to which this ship belongs.
     */
	 @Override
    public void doAction(SpaceWars game){
    	
    	this.game = game;
    	this.teleport();
    	this.specialBehavior(game);
    	this.shieldOn();
    	this.fire(game);

    	this.setCurrentEnergy(Energy.CONSTANTLY_CHARGING);
    }
	
	/**
	 * return the image of HumanControlled ship with or without shield
	 * @return image object 
	 */
	 @Override
	public Image getImage() {
		return this.currentImageShip;		
	}

	/**
	 * Attempt to do a shot.
	 */
	 @Override
	public void fire(SpaceWars game) {
		if (game.getGUI().isShotPressed()) {
			
			super.fire(game);
			
		}	
	}
	
	/**
	 * Attempt to put a shield on. 
	 */
	 @Override
	public void shieldOn() {
		
		if(this.game.getGUI().isShieldsPressed()){
			
			super.shieldOn(); // will check if there is enough energy
			if (this.getShield().isSheildActivated())
				this.currentImageShip = GameGUI.SPACESHIP_IMAGE_SHIELD; // put shield on
				return;
		}
		
		this.currentImageShip = GameGUI.SPACESHIP_IMAGE; // down the shield
	}

	/**
	 * Attempt to do a teleport.
	 */
	 @Override
	public void teleport() {
		
		if(this.game.getGUI().isTeleportPressed()){
			super.teleport();
		}
		
	}

	/**
	 * Attempt to do a turn or acceleration as human player can do.
	 */
	private void specialBehavior(SpaceWars game) {

		boolean accelerate = false;
		int turn = NO_TURN;
		
		if(this.game.getGUI().isUpPressed())
			accelerate = true;
		
		if (this.game.getGUI().isLeftPressed())
			turn = TURN_LEFT;
		else if (this.game.getGUI().isRightPressed())
			turn = TURN_RIGHT;
		
		this.getPhysics().move(accelerate, turn);
	}
}