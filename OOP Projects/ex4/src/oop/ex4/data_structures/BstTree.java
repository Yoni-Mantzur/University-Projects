package oop.ex4.data_structures;

/**
 * This class represent a binary search tree.
 * 
 * @author YONI
 *
 */
class BstTree {

	/** The depth of non vertex or root */
	public static final int DEPTH_NON_VERTEX = -1, DEPTH_OF_ROOT = 0, HEIGHT_LEAF = 0;
	/** No items in tree */
	public static final int EMPTY_TREE = 0;
	/** Represent the numbers of children for a vertex */
	public static final int ONE_SON = 1, TWO_SONS = 2, NO_SONS = -1;
	
	
	// The root of the tree.
	private IntegerBstNode root;
	// Contains the item that we want to do operation on.
	private IntegerBstNode IntegerBstNodeParentElementToAdd, IntegerBstNodeElementToDelete;
	// The number elements in the tree.
	private int size;
	// Counter the depth of searching node.
	private int counterDepthOfSearchingNode;

	
	/**
	 * Constructor.
	 */
	public BstTree() {
		
		this.root = null;
		this.size = EMPTY_TREE;
		this.counterDepthOfSearchingNode = DEPTH_NON_VERTEX;
	}
	
	/**
	 * Constructor.
	 * 
	 * @param newHead - the newRoot of the tree.
	 * @param size - the number of elements in the tree.
	 */
	public BstTree(IntegerBstNode newHead, int size){
		
		this.root = newHead;
		this.size = size;
		this.counterDepthOfSearchingNode = DEPTH_NON_VERTEX;
	}
	
			
	/**
	 * Find the min in the tree.
	 * 
	 * @param head - the root of the tree.
	 * @return
	 */
	 public  IntegerBstNode tree_min(IntegerBstNode head){
		
		 IntegerBstNode currentIntegerBstNode = head;
			
		 while (currentIntegerBstNode.getLeft() != null ) // The min in the tree is the most left leaf.
			 currentIntegerBstNode = currentIntegerBstNode.getLeft();
		 return currentIntegerBstNode;
	}

	/**
	 * Check if some number in the tree.
	 * 
	 * @param searchValue - the searching number
	 * @return true if the number in the tree, false otherwise.
	 */
	public int contain(int searchValue){
		
		this.counterDepthOfSearchingNode = DEPTH_OF_ROOT;
		
		this.findPlace(this.root, searchValue);
		
		if ((this.IntegerBstNodeElementToDelete != null) && 
					(this.IntegerBstNodeElementToDelete.getValue() == searchValue))
			return this.counterDepthOfSearchingNode;
		
		return DEPTH_NON_VERTEX;
	}
	
	/*
	 * Check if searchValue in the tree, if so mark it as optional to delete, if not mark the place 
	 * as optional to add.
	 */
	private IntegerBstNode findPlace(IntegerBstNode head , int searchValue){
			
			
			if (head == null){

				return null;
				
			} else if (head.getValue() ==  searchValue){
				
				this.IntegerBstNodeElementToDelete = head;
		
			} else if (head.getValue() < searchValue){
				this.IntegerBstNodeParentElementToAdd = head;
				counterDepthOfSearchingNode++;
				return findPlace(head.getRight(), searchValue);
		
			} else {
				this.IntegerBstNodeParentElementToAdd = head;
				counterDepthOfSearchingNode++;
				return findPlace(head.getLeft(), searchValue);
			}
			
			return null;
	}
		
	/**
	 * Add item to the tree in the place will save the bst order.
	 * 
	 * @param addValue
	 * @return
	 */
	public IntegerBstNode add(int addValue){
		
		if (this.contain(addValue) != DEPTH_NON_VERTEX)
			return null;
		
		//Add it as a new leaf.
		IntegerBstNode newIntegerBstNode = new IntegerBstNode(addValue,this.IntegerBstNodeParentElementToAdd, 
																						null, null,0);
		
		if (this.root == null)
			this.root = newIntegerBstNode;
		
		else if (this.IntegerBstNodeParentElementToAdd.getValue() > addValue)
			this.IntegerBstNodeParentElementToAdd.setLeft(newIntegerBstNode);
		else
			this.IntegerBstNodeParentElementToAdd.setRight(newIntegerBstNode);
		
		this.size++;
		updateHeights(newIntegerBstNode);
		return newIntegerBstNode;
	}
	
	
	/**
	 * Find the successor of some number that in the tree.
	 * 
	 * @param IntegerBstNodeInBst - the IntegerBstNode number looking for successor.
	 * @return - the successor of IntegerBstNodeInBst
	 */
	public IntegerBstNode successor(IntegerBstNode IntegerBstNodeInBst){
		
		// If has right son, return the max of his right son tree.
		if (IntegerBstNodeInBst.getRight() != null)
			return tree_min(IntegerBstNodeInBst.getRight());
		
		// If not has right son, if its the max of the tree, not have successor (means return null)
		// point that the deletion will not get to here cuse it's a leaf.
		// otherwise, return the IntegerBstNode that IntegerBstNodeInBst his the left son of his.
		IntegerBstNode successorOf = IntegerBstNodeInBst.getParent();
		
		while(successorOf !=  null && IntegerBstNodeInBst == successorOf.getRight()){
			IntegerBstNodeInBst = successorOf;
			successorOf = successorOf.getParent();
		}
		return successorOf;	
	}
	
	/*
	 * Help function to delete element that is in the tree, the delete function call to this function
	 * with the element IntegerBstNode and the code of the situation - with 2 sons, 1 son or none, and handle each
	 * situation.
	 */
	private boolean deletionIntegerBstNode(IntegerBstNode IntegerBstNodeToDelete, int caseOfDeletion){
		
		switch (caseOfDeletion){
			// If no sons just remove it.
			case NO_SONS:
				if (this.root == IntegerBstNodeToDelete)
					this.root = null;
				else if (isRightChild(IntegerBstNodeToDelete))
					IntegerBstNodeToDelete.getParent().setRight(null);
				else
					IntegerBstNodeToDelete.getParent().setLeft(null);
				return true;
				
				// If one son, connect his parent with his son.	
			case ONE_SON:
				
				if (isRightChild(IntegerBstNodeToDelete))
					IntegerBstNodeToDelete.getParent().setRight((IntegerBstNodeToDelete.getRight() != null) ? 
											IntegerBstNodeToDelete.getRight() : IntegerBstNodeToDelete.getLeft());
				else
					IntegerBstNodeToDelete.getParent().setLeft((IntegerBstNodeToDelete.getRight() != null) ? 
											IntegerBstNodeToDelete.getRight() : IntegerBstNodeToDelete.getLeft());
				return true;
			
			// If two sons using successor
			case TWO_SONS:
				
				IntegerBstNode secceorOfItemToDelete = successor(IntegerBstNodeToDelete);
				IntegerBstNodeElementToDelete.setValue(secceorOfItemToDelete.getValue());
				IntegerBstNodeElementToDelete = secceorOfItemToDelete;
				// We proofed that for this successor, will be only right son at most.
				return (deletionIntegerBstNode(secceorOfItemToDelete, manySons(secceorOfItemToDelete)));			
				
			default: // Not supposed to get here.
				return true;	
		}
	}
	/**
	 * Delete an item in the tree.
	 * 
	 * @param itemToDelete - the number we want to delete.
	 * @return - the parent of the item deleted, null otherwise, means the item is not in the tree.
	 */
	public IntegerBstNode delete(int itemToDelete){
		
		if (this.contain(itemToDelete) == DEPTH_NON_VERTEX)
			return null;
		
		int manySonsOfDeletElement = manySons(this.IntegerBstNodeElementToDelete);
		
		if (manySonsOfDeletElement == NO_SONS)			
			deletionIntegerBstNode(this.IntegerBstNodeElementToDelete, NO_SONS);
		
		else if (manySonsOfDeletElement == ONE_SON)
			deletionIntegerBstNode(this.IntegerBstNodeElementToDelete, ONE_SON);
				
		else 		
			deletionIntegerBstNode(this.IntegerBstNodeElementToDelete, TWO_SONS);
		
		this.size--;
		updateHeights(IntegerBstNodeElementToDelete.getParent());
		return this.IntegerBstNodeElementToDelete.getParent();
		
	}
	
	/**
	 * @return - the head of the tree.
	 */
	public IntegerBstNode getHead(){
		return this.root;
	}
	
	
	
	/**
	 * Update the heights of the leaf it gets to the head of tree. Using after deletion and adding.
	 */
	public void updateHeights(IntegerBstNode node){
		
		while (node != null){
			if (node.getLeft() == null && node.getRight() == null)			
				node.setHiehgt(HEIGHT_LEAF);
		
			else if (node.getLeft() == null)
				node.setHiehgt(node.getRight().getHeight() + 1);
		
			else if (node.getRight() == null)
				node.setHiehgt(node.getLeft().getHeight() + 1);
			else
				node.setHiehgt(Math.max(node.getLeft().getHeight(), node.getRight().getHeight()) + 1 );
			node = node.getParent();
		}
	}
	
	/**
	 * The function get node, and return how many sons he has and what sons are they (left or right)
	 * 
	 * @param node - checked how many sons it has.
	 * @return the number of sons.
	 */
	public static int manySons(IntegerBstNode node){
		
		if ((node.getLeft() == null) && (node.getRight() == null))
			return NO_SONS;
		
		if (node.getRight() == null || node.getLeft() == null)
			return ONE_SON;
		
		return TWO_SONS;
	}
		
	/**
	 * @return the number of nodes in the tree.
	 */
	public int size(){
		
		return this.size;
	}
	
	
	/**
	 * Check if node is right child of his parent.
	 * 
	 * @param node - the node we check if it's right son (not the root).
	 * @return true if so, false otherwise.
	 */
	public static boolean isRightChild(IntegerBstNode node){
		
		return node.getParent().getValue() <= node.getValue();
	}
}
