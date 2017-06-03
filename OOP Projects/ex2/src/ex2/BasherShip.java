package ex2;

import java.awt.Image;

import oop.ex2.GameGUI;

/**
 * The Class represent a Basher ship, trying to fly after the nearest ship and if 
 * it answer the precautions warning it will put the shield on!
 * 
 * @see EnemyShip
 * @see SpaceShip
 * @author YONI
 *
 */
public class BasherShip extends EnemyShip {
	
	private Image currentImageShip;
	private SpaceWars game;


	public BasherShip() {
		
		super();
		this.currentImageShip = GameGUI.ENEMY_SPACESHIP_IMAGE;

	}

    /**
     * Does the actions of this ship for this round. The ship trying to run after the nearest ship and 
     * put on the shield when it to close.  
     * This is called once per round by the SpaceWars game driver.
     * 
     * @param game the game object to which this ship belongs.
     */
	@Override
	public void doAction(SpaceWars game) {
		
		this.game = game;
		
		this.specialBehavior(game);
		this.shieldOn();
		this.setCurrentEnergy(Energy.CONSTANTLY_CHARGING);
	}

    /**
     * Gets the image of this ship. This method should return the image of the
     * ship with or without the shield. This will be displayed on the GUI at
     * the end of the round.
     * 
     * @return the image of this ship.
     */
	@Override
	public Image getImage() {
		
		return this.currentImageShip;
	}
	
    /**
     * Attempts to turn on the shield. Just if it answer the precautions warning!
     */
	@Override
	public void shieldOn(){
		
		if (this.getPrecautions.isDistanceBreak(this.game, this)){
			super.shieldOn();
		}
	}
	
	/* The special behavior is to run after the closest ship */
	private void specialBehavior(SpaceWars game) {
		
		this.runAfterNearestShip(game);
	}

}
