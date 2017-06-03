package oop.ex4.data_structures;

/**
 * 
 * Abstract class that charge on checking balance of Avl tree, what violation is in it, and the fixing methods.
 * 
 * @See AvlTree
 * @author YONI
 *
 */
abstract class AvlOutOfBalance {

	/** The represent numbers of the kind of violation */
	public static final int VAIOLATION_RR = 1, VAIOLATION_RL = 2, VAIOLATION_LL = 3, VAIOLATION_LR = 4, 
																						NO_VAIOLATION = 0;
	
	/* Represent numbers of what violation is in given node regard to his sons*/
	private static int FIRST_RIGHT_VIOLATION = -2, FIRST_LEFT_VIOLATION = 2, SECOND_RIGHT_VIOLATION = -1,
																				  SRCOND_LEFT_VIOLATION = 1;
	
	/**
	 * Check if there is a violation in this node, and if so, return the kind of.
	 * 
	 * @param node - the node that checking.
	 * @return the kind of violation that occur, 0 if no violation.
	 */
	public static int isAvlBrokeHere(IntegerBstNode node){
		
		// Using the checkBlanced method to check what the balance in the node.
		int checkBalanceNode = checkBlanced(node);
		
		if (checkBalanceNode == FIRST_RIGHT_VIOLATION){
			
			if (checkBlanced(node.getRight()) == SRCOND_LEFT_VIOLATION)
				return VAIOLATION_RL;
			return VAIOLATION_RR;		
			
		} else if (checkBalanceNode == FIRST_LEFT_VIOLATION)
		{
			if (checkBlanced(node.getLeft()) == SECOND_RIGHT_VIOLATION)
				return VAIOLATION_LR;
			return VAIOLATION_LL;
		}
		
		return NO_VAIOLATION;				
	}
	
	/*
	 * Method to check what the balance in the node.
	 */
	private static int checkBlanced(IntegerBstNode node){
		
		int manySonsOfNode = BstTree.manySons(node);
		
		switch (manySonsOfNode){
		
			case BstTree.TWO_SONS:
				return (node.getLeft().getHeight() - node.getRight().getHeight());
			
			case BstTree.ONE_SON: 
				if (node.getLeft() == null)
					return (BstTree.DEPTH_NON_VERTEX - node.getRight().getHeight());
				return (node.getLeft().getHeight() - BstTree.DEPTH_NON_VERTEX);
				
			case BstTree.NO_SONS:
				return NO_VAIOLATION;
				
			default: return NO_VAIOLATION; // not supposed to get here.
		}
			
	}
	
	private static void setHieghtAfterFixing(IntegerBstNode voilatingIntegerBstNode){
		
		if (BstTree.manySons(voilatingIntegerBstNode) == BstTree.NO_SONS)
			
			voilatingIntegerBstNode.setHiehgt(Math.max(voilatingIntegerBstNode.getParent().getHeight()-2, 0));
		else
			voilatingIntegerBstNode.setHiehgt(Math.max(voilatingIntegerBstNode.getParent().getHeight()-1, 0));
		
		
	}
	
	/**
	 * The function rotating left for RR Violation.
	 * 
	 * @param voilatingIntegerBstNode - the IntegerBstNode that violated
	 * @return the IntegerBstNode after fixing.
	 */
	public static IntegerBstNode fixRRviolation(IntegerBstNode voilatingIntegerBstNode){
		
		IntegerBstNode fixNode = voilatingIntegerBstNode.getRight();
		voilatingIntegerBstNode.setRight(fixNode.getLeft());
		
		if (fixNode.getLeft() != null)
			fixNode.getLeft().setParent(voilatingIntegerBstNode);
		
		//Rotate left the violated node.
		fixNode.setParent(voilatingIntegerBstNode.getParent());
		fixNode.setLeft(voilatingIntegerBstNode);
		voilatingIntegerBstNode.setParent(fixNode);
		
		setHieghtAfterFixing(voilatingIntegerBstNode);
		
		return fixNode;
	}
	
	/**
	 * The function rotating right for LL Violation.
	 * 
	 * @param voilatingIntegerBstNode - the IntegerBstNode that violated.
	 * @return the IntegerBstNode after fixing.
	 */
	public static IntegerBstNode fixLLviolation(IntegerBstNode voilatingIntegerBstNode){
		
		
		IntegerBstNode fixNode = voilatingIntegerBstNode.getLeft();
		
		voilatingIntegerBstNode.setLeft(fixNode.getRight());
		
		if (fixNode.getRight() != null)
			fixNode.getRight().setParent(voilatingIntegerBstNode);
		
		//Rotate right the violated node.
		fixNode.setParent(voilatingIntegerBstNode.getParent());
		fixNode.setRight(voilatingIntegerBstNode);
		voilatingIntegerBstNode.setParent(fixNode);
		
		setHieghtAfterFixing(voilatingIntegerBstNode);
		
		return fixNode;
		
	}
	
	
	/**
	 * The function rotating right for his son and then left for him for RL Violation.
	 * 
	 * @param voilatingIntegerBstNode - the IntegerBstNode that violated.
	 * @return the IntegerBstNode after fixing.
	 */
	public static IntegerBstNode fixRLviolation(IntegerBstNode root,IntegerBstNode voilatingIntegerBstNode){
		
		boolean isRightSon;
		if (root == voilatingIntegerBstNode)
			isRightSon = true;
		else
			isRightSon = BstTree.isRightChild(voilatingIntegerBstNode.getRight());
		
		IntegerBstNode fixIntegerBstNode = AvlOutOfBalance.fixLLviolation(voilatingIntegerBstNode.getRight());
			
		updateParentAfterFixing(fixIntegerBstNode, isRightSon);
		
		fixIntegerBstNode = AvlOutOfBalance.fixRRviolation(fixIntegerBstNode.getParent());
		
		
		
		return fixIntegerBstNode;
		
	}
	
	/**
	 * The function rotating left for his son and then right for him for LR Violation.
	 * 
	 * @param voilatingIntegerBstNode - the IntegerBstNode that violated.
	 * @return the IntegerBstNode after fixing.
	 */
	public static IntegerBstNode fixLRviolation(IntegerBstNode root, IntegerBstNode voilatingIntegerBstNode){
		
		boolean isRightSon;
		if (root == voilatingIntegerBstNode)
			isRightSon = false;
		else
			isRightSon = BstTree.isRightChild(voilatingIntegerBstNode.getLeft());
		
		IntegerBstNode fixIntegerBstNode = AvlOutOfBalance.fixRRviolation(voilatingIntegerBstNode.getLeft());
		
		updateParentAfterFixing(fixIntegerBstNode, isRightSon);
		
		fixIntegerBstNode = AvlOutOfBalance.fixLLviolation(fixIntegerBstNode.getParent());
		
		return fixIntegerBstNode;
		
	}
	
	/**
	 * Update the parent of the given node after fixing it.
	 * 
	 * @param fixNode - the node was fixed.
	 * @param isRightSon - tells if it's right son (true) or left (false).
	 */
	public static void updateParentAfterFixing(IntegerBstNode fixNode, boolean isRightSon) {
		
		if(isRightSon)
			fixNode.getParent().setRight(fixNode);
		else
			fixNode.getParent().setLeft(fixNode);
		
	}

}
