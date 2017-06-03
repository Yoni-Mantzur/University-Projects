package oop.ex4.data_structures;

/*
 * Class that represent a IntegerBstNode in the tree.
 * 
 * @author YONI
 *
 */
class IntegerBstNode{

	private IntegerBstNode parent, right, left;

	private int value, height;
		
	/**
	 * Constructor.
	 * 
	 * @param value - the value of the IntegerBstNode.
	 * @param parent - the patent of this IntegerBstNode.
	 * @param right - the right son of this IntegerBstNode.
	 * @param left - the left son of this IntegerBstNode.
	 */
	public IntegerBstNode(int value, IntegerBstNode parent, IntegerBstNode right, IntegerBstNode left, int height){
			
			this.value = value;
			this.parent = parent;
			this.right = right;
			this.left = left;
			this.height = height;
	}
	
	/**
		 * @return - the parent of the IntegerBstNode.
		 */
		protected IntegerBstNode getParent(){
			
			return this.parent;
		}
		
		/**
		 * @return the right son of the IntegerBstNode.
		 */
		protected IntegerBstNode getRight(){
			
			return this.right;
		}
		
		/**
		 * @return the left son of the IntegerBstNode.
		 */
		protected IntegerBstNode getLeft(){
			
			return this.left;
			
		}
		
		/**
		 * @return the value of the IntegerBstNode.
		 */
		protected int getValue(){
			
			return this.value;
			
		}
		
		/**
		 * @return the height of the IntegerBstNode.
		 */
		protected int getHeight(){
			
			return this.height;
		}
		
		/**
		 * Set a new value for the IntegerBstNode.
		 * 
		 * @param newParent - the new parent.
		 */
		protected void setValue(int newValue){
			
			this.value = newValue;
		}
		
		
		/**
		 * Set a new parent for the IntegerBstNode.
		 * 
		 * @param newParent - the new parent.
		 */
		protected void setParent(IntegerBstNode newParent){
			
			this.parent = newParent;
		}
		
		/**
		 * Set a new right son for the IntegerBstNode.
		 * 
		 * @param newRight - the new right son.
		 */
		public void setRight(IntegerBstNode newRight){
			
			this.right = newRight;
		}
		
		/**
		 * Set a new left son for the IntegerBstNode.
		 * 
		 * @param newLeft - the new left son.
		 */
		public void setLeft(IntegerBstNode newLeft){
			
			this.left = newLeft;
			
		}
		
		/**
		 * Set a new height for the IntegerBstNode.
		 * 
		 * @param newHight - the new newHight.
		 */
		public void setHiehgt(int newHight){
			
			this.height = newHight;
			
		}
}
