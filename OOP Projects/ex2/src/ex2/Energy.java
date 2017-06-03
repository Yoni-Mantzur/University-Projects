package ex2;

/**
 * Interface represent the measure of energy object can be with.
 * @author YONI
 *
 */
public interface Energy {
	
	/** The start energy. */
	public static final int START_ENERGY = 200;
	/** The least energy object can be with. */
	public static final int MINIMAL_ENERGY = 0;
	/** Bashing - Factor additional to Energy when object with shield has been collided with other object. */
	public static final int BASHING_IMPACT = 20;
	/** Factor additional to Energy when object has been got hit or been collided with no shield. */
	public static final int GOT_HITTING_IMPACT = -10;
	/** Factor additional to Energy when object fire. */
	public static final int FIRRING_IMPACT = -20;
	/** Factor additional to Energy when object has been transposed. */
	public static final int TARNSPOSED_IMPACT = -150;
	/** Constantly deduction of energy. */
	public static final int CONSTANTLY_CHARGING = 1;
	/** Factor additional to Energy when object has been used shield. */
	public static final int SHIELD_USE = -3;
	
	/**
	 * Get the current energy of this object.
	 * @return the current energy
	 */
	public int getCurrentEnergy();
	
	/**
	 * Set new current energy.
	 * @param addFactor - additional value for the current energy.
	 */
	public void setCurrentEnergy(int addFactor);
	
	/**
	 * Get the max energy of this object.
	 * @return the max energy
	 */
	public int getMaxEnergy();
	
	/**
	 * Set new max energy.
	 * @param addFactor - additional value for the max energy.
	 */
	public void setMaxEnergy(int addFactor);
	
}
