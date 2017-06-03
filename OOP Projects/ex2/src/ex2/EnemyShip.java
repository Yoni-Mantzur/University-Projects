package ex2;

import java.awt.Image;

import oop.ex2.GameGUI;

/**
 * The Class represent an abstract enemy ship (means not human controlled).
 * 
 * @see SpaceShip
 * @author YONI
 *
 */
public abstract class EnemyShip extends SpaceShip {
	
	/** Always accelerates! */
	public static boolean ACCELERATION = true;
	/** Each enemy ship has a Precautions warning! */
	protected Precautions getPrecautions;

	private Image currentImage;
	
	/**
	 * Constructor
	 */
	public EnemyShip() {
		
		getPrecautions = new Precautions(); // Composition
		this.currentImage = GameGUI.ENEMY_SPACESHIP_IMAGE;
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
		
		return this.currentImage;
	}
	
    /**
     * Attempts to turn on the shield. Just if it answer the precautions warning!
     */
	@Override
	public void shieldOn(){
		
			super.shieldOn();
		
			if (this.getShield().isSheildActivated()){
				this.currentImage = GameGUI.ENEMY_SPACESHIP_IMAGE_SHIELD;
				
			} else {
				this.currentImage = GameGUI.ENEMY_SPACESHIP_IMAGE;
			}		
	}
	
	/**
	 * This method get an Enemy ship in a  current game and trying to get close to the nearst ship.
	 * @param game - the current game is play
	 * @param enemyship - Enemy ship that will get closer.
	 */
	protected void runAfterNearestShip(SpaceWars game){
		
		SpaceShip nearestShip = game.getClosestShipTo(this);
		
		if (this.getPhysics().angleTo(nearestShip.getPhysics()) <= 0)
			this.getPhysics().move(ACCELERATION, TURN_RIGHT);
		else
			this.getPhysics().move(ACCELERATION, TURN_LEFT);	
	}

}
