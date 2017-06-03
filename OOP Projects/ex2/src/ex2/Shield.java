package ex2;

/**
 * Class represent a shield object.
 * @author YONI
 *
 */
public class Shield{

	private boolean isShieldActive;
	
	/**
	 * Constructor of shield object.
	 * 
	 */
	public Shield() {
		
		this.isShieldActive = false; 	
	}
	
	/**
	 * Turn on the shield.
	 */
	public void activeSheild(){
		this.isShieldActive = true;
	}
	
	/**
	 * Turn off the shield.
	 */
	public void turnOff(){
		this.isShieldActive = false;
	}
	
	/**
	 * Is the shield was turned on?
	 * @return true if is on, false if is off.
	 */
	public boolean isSheildActivated(){
		
		return this.isShieldActive;
	}

}
