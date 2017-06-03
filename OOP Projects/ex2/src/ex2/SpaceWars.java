package ex2;

import java.util.ArrayList;
import oop.ex2.*;

/**
 * This class acts as the driver for the Space Wars game. It is part of Ex57
 * (see the exercise description for more details).
 * 
 * @author oop
 */
public class SpaceWars{
    
    /** The human-controlled spaceship type*/
    public static final int HUMAN_CONTROLLED_SHIP = 0;
    
    /** The floating spaceship type*/
    public static final int FLOATING_SHIP = 1;
    
    /** The runner spaceship type*/
    public static final int RUNNER_SHIP = 2;
    
    /** The aggressive spaceship type*/
    public static final int AGGRESSIVE_SHIP = 3;
    
    /** The basher spaceship type*/
    public static final int BASHER_SHIP = 4;

    /** The special ship you designed yourself*/
    public static final int SPECIAL_SHIP = 5;
  
    /** The number of rounds a shot will exist after being fired.*/
    private static final int SHOT_TIME_TO_LIVE = 40;
    
    /** The Graphical user interface used to display the game, and get input.*/
    private GameGUI gui;
    
    /** The array of spaceships that participate in the game.*/
    private SpaceShip[] ships;
    
    /** A list of all shots that have been fired and still exist in the game.*/
    private ArrayList<ShotPhysics> shots;
    
    /** 
     * An array that specifies the number of time each spaceship has died in
     * the game.
     */
    private int[] deathCount;
    
    /**
     * Creates a new game.
     * 
     * @param args the command line arguments that indicate which types of
     * spaceships to add to the game.
     */
    public SpaceWars(String[] args){
        this.ships = createSpaceShips(args);
        if (this.ships==null || this.ships.length<1) {
            printUsageAndExit();
        }
        for (int i=0;i<this.ships.length; i++) {
            if(this.ships[i]==null) {
                printUsageAndExit();
            }
        }
        deathCount = new int[this.ships.length];
        this.gui = new GameGUI();
        this.shots = new ArrayList<ShotPhysics>();
        postDeathCountToGUI();
    }
    
    /**
     * Creates the spaceships in the game.
     * 
     * @param args the command line arguments.
     * @return the array of spaceships.
     */
    private SpaceShip[] createSpaceShips(String[] args) {
        return SpaceShipFactory.createSpaceShips(args);
    }

    /**
     * Prints a usage message that explains how to run the game.
     */
    private static void printUsageAndExit() {
        System.out.println("Usage: \n" + 
                           "\tjava SpaceWars <spaceship types>\n\n"+
                           "Available spaceship types:\n"+
                           "\th - Human\n"+
                           "\td - Drunkard\n"+
                           "\tr - Runner\n"+
                           "\ta - Aggressive\n"+
                           "\tb - Basher\n\n"+
                           "\ts - Special\n\n"+
                           "You must supply at least two spaceship types,"+
                           " and the human type can only appear once.");
        System.exit(1);
    }

    /**
     * runs the game.
     */
    private void run() {
        while(!this.gui.isEscPressed()){
            moveSpaceShips();
            moveShots();
            checkCollisions();
            checkHits();
            drawAllObjects();
            removeDeadShots();
            resetDeadShips();
        }
    }

    /**
     * does the action of all spaceships in this round by calling their
     * doAction() method.
     */
    private void moveSpaceShips() {
        for(int i=0; i<this.ships.length; i++){
            this.ships[i].doAction(this);
        }
    }

    /**
     * removes shots that have expired.
     */
    private void removeDeadShots() {
        for(int i=this.shots.size()-1; i>=0; i--){
            if( this.shots.get(i).expired()){
                this.shots.remove(i);
            }
        }
    }

    /**
     * Checks to see if a shot has hit a space ship.  If one did hit, then the
     * ship's gotHit() method is called, and the shot is removed.
     */
    private void checkHits() {
        for(int i=this.shots.size()-1; i>=0; i--){
            for(int j=0; j<this.ships.length; j++){
                if(this.shots.get(i).hits(this.ships[j].getPhysics())){
                    this.ships[j].gotHit();
                    this.shots.remove(i);
                    break;
                }
            }
        }
    }

    /**
     * Updates the position of all the shots in the game.
     */
    private void moveShots() {
        for(int i=this.shots.size()-1; i>=0; i--){
            this.shots.get(i).move();
        }
    }

    /**
     * Goes over all ships, and checks if they are dead. If so, their reset
     * method is called.
     */
    private void resetDeadShips() {
        for(int i=0; i<this.ships.length; i++){
            if(this.ships[i].isDead()){
                deathCount[i]++;
                this.ships[i].reset();
                postDeathCountToGUI();
            }
        }
    }

    /**
     * displays on the GUI the number of times each of the players has died.
     */
    private void postDeathCountToGUI() {
        String text = "";
        for(int i=0; i<deathCount.length; i++){
            text += "P" + (i+1) + ": " + deathCount[i] + "   ";
        }
        this.gui.setText(text);
        
    }

    /**
     * Draws all spaceships and shots on the GUI.
     */
    private void drawAllObjects() {
        for(int i=0; i<this.ships.length; i++){
            this.gui.addImageToBuffer(this.ships[i].getImage(), this.ships[i].getPhysics());
        }
        for(int i=this.shots.size()-1; i>=0; i--){
            this.gui.addImageToBuffer(GameGUI.SHOT_IMAGE, this.shots.get(i));
        }
        this.gui.drawBufferToScreen();
    }



    /**
     * Checks for collisions between spaceships. If two spaceships collide,
     * their speeds are adjusted, and the collideWithSpaceShip() method of each
     * spaceship is called.
     */
    private void checkCollisions() {
        for(int i=0; i<this.ships.length; i++){
            for(int j=i+1; j<this.ships.length; j++){
                if(this.ships[i].getPhysics().testCollisionWith(this.ships[j].getPhysics())){
                    this.ships[i].collidedWithAnotherShip();
                    this.ships[j].collidedWithAnotherShip();
                }    
            }
        }
    }

    /**
     * Gets the GUI object we are drawing with. This method can be used by 
     * the spaceships to obtain the GUI for their own use.
     * 
     * @return the gui object.
     */
    public GameGUI getGUI() {
        return this.gui;
    }

    /**
     * Fires a new shot from the current location of the spaceship.  The shot
     * will automatically be managed by the SpaceWars game object.
     * 
     * @param position the position of the firing spaceship.
     */
    public void addShot(SpaceShipPhysics position) {
        this.shots.add(new ShotPhysics(position,SHOT_TIME_TO_LIVE));
    }

    /**
     * returns the ship that is closest to the given one.
     * 
     * @param ship the given ship
     * @return the closest ship to the given one.
     */
    public SpaceShip getClosestShipTo(SpaceShip ship) {
        double maxDistance = Double.MAX_VALUE;
        SpaceShip closest = null;
        for(int i=0; i<this.ships.length; i++){
            if(this.ships[i]!=ship){
                double distance = this.ships[i].getPhysics().distanceFrom(ship.getPhysics());
                if(distance < maxDistance){
                    closest = this.ships[i];
                    maxDistance = distance;
                }
            }
        }
        return closest;
    }
    
    /**
     * Runs the game.
     * 
     * @param args command line arguments. These should describe the type of
     * the spaceships in the game.  See the exercise description for details.
     */
    public static void main(String[] args){
        SpaceWars game = new SpaceWars(args);
        game.run();
    }
}
