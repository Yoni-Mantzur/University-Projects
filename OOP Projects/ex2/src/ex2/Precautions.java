package ex2;


/**
 * Class represent the precautions Enemy ships need to be aware as the SpaceWars game is written.
 * 
 * @see SpaceWars
 * @author  Yoni 
 */
public class Precautions{
	
	/** The ship left only 10 points life */
	public static final int LIFE_IN_DANGER = 10;
	/** Limit the distance and angel from the near ship from special attack */
	public static final double LIMIT_DISTANCE = 0.2, LIMIT_ANGEL = 0.2;
	
		
	/**
	 * This method will get a enemy ship and in current game and check if there is a spaceship near it 
	 * over the distance limit.  
	 * 	
	 * @param game - a current game is playing.
	 * @param EnemyShip - the ship we want to check.
	 * @return true if there if ship near over the limit, else otherwise.
	 */
	protected boolean isDistanceBreak(SpaceWars game, EnemyShip EnemyShip){
		
		SpaceShip  closestShip =  game.getClosestShipTo(EnemyShip);
		double distanceFromClosestShip = EnemyShip.getPhysics().distanceFrom(closestShip.getPhysics());
		
		if (distanceFromClosestShip < LIMIT_DISTANCE)
			return true;
		return false;
	}
	
	/**
	 * This method will get a enemy ship and in current game and check if there is a spaceship with angle
	 * over the angle limit.  
	 * 	
	 * @param game - a current game is playing.
	 * @param EnemyShip - the ship we want to check.
	 * @return true if there if ship near over the limit, else otherwise.
	 */
	protected boolean isAngelBreak(SpaceWars game, SpaceShip EnemyShip){
		

		SpaceShip  closestShip =  game.getClosestShipTo(EnemyShip);
		double angleClosestShip = EnemyShip.getPhysics().angleTo(closestShip.getPhysics());
		
		if (Math.abs(angleClosestShip) < LIMIT_ANGEL)
			return true;	
		return false;
		
		
	}
	
	


}
