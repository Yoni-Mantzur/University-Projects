package ex2;


/**
 * Interface represent the ability to run a shot.
 * 
 * @author YONI
 */
public interface Shootable {
	
	/** The shoot can be made only after 8 rounds from shooting. */
	public static final int LIMIT_SHOOT_PER_ROUNDS = 8;
	
	/**
	 * Function that responsible of attempt of shooting.
	 * @param game - the game will shoot at.
	 */
	public abstract void fire(SpaceWars game);
	
	/**
	 * Function that check if it can be a attempt of shooting. 
	 * @return true if so or false if not passed 8 rounds or there is no energy
	 */
	public boolean isFiredAvailable();
	
	

}
