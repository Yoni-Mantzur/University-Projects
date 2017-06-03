package ex2;

/**
 * @author YONI
 *
 */
public interface Health {
	
	/** The start energy. */
	public static final int START_HEALTH = 20;
	/** The least energy object can be with. */
	public static final int MINIMAL_HEALTH = 0;
	/** Factor additional to Health when object has been got hit or been collided with no shield. */
	public static final int GOT_HITTING_IMPACT = -1;
	
	
	/**
	 * Get the current Health points of this object.
	 * @return the current energy
	 */
	public int getCurrentHealth();
	
	/**
	 * Set new current Health points.
	 * @param addFactor - additional value for the current energy.
	 */
	public void setCurrentHealth(int addFactor);
}
