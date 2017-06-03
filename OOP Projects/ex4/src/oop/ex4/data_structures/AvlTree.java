package oop.ex4.data_structures;

import java.util.Iterator;
import java.util.NoSuchElementException;


/**
 * Class represent an AVL tree structure.
 * 
 * @see IntegerBstNode
 * @see BstTree
 * @author YONI
 *
 */
class AvlTree implements Iterable<Integer> {
	
		
	/*
	 * An Iterator that goes over the numbers in the tree as sorting way.
	 */
	private class AvlTreeIterator implements Iterator<Integer>{
		
		private int sizeIterator;
		private IntegerBstNode nextNode, currentNode;
		
		
		/**
		 * Constructor.
		 * @param size - the size of the current elements in the tree
		 * @param minimalNode - the minimal node in the tree.
		 */
		public AvlTreeIterator(int size, IntegerBstNode minimalNode){
			
			this.sizeIterator = size;
			this.currentNode = minimalNode;
			this.nextNode = bstTree.successor(minimalNode);
			
		}
		
		@Override
		public boolean hasNext() {

			return sizeIterator > BstTree.EMPTY_TREE;
		}

		@Override
		/**
		 * The next successor number
		 */
		public Integer next() {

			if (!this.hasNext())
				throw new NoSuchElementException();
			
			int currentValue = this.currentNode.getValue();
			this.currentNode = this.nextNode;
			
			// If null means maximum of tree send.
			this.nextNode = (this.currentNode == null) ? null : bstTree.successor(currentNode);
			
			sizeIterator--;
			return currentValue;
		}

		@Override
		/**
		 * Does not supporting in remove.
		 */
		public void remove() {
			throw new UnsupportedOperationException();			
		}
		
		
	}
	
	//// The AvlTree Class //////
	
	private static final int CHECK_AFTER_ADDING = 1, CHECK_AFTER_DELETE = 2;
	
	// The bstTree we 'decorating'.
	private BstTree bstTree;


	/**
	 * The default constructor.
	 */
	public AvlTree() {
		
		this.bstTree = new BstTree();
	}
	
	/**
	 * A constructor that builds the tree by adding the elements in the input array one by one.
	 * If the value appears more than once in the least, the first appearance is added.
	 * 
	 * @param data - the value to add to tree.
	 */
	public AvlTree(int[] data){
		
		this.bstTree = new BstTree();
		for (int item : data)
			this.add(item);
	}
	
	/**
	 * A copy constructor that creates a deep copy of the given AvlTree. This means that for every node
	 * or any other internal object of the given tree, a new, identical object, is instantiated for the 
	 * new tree (the internal object is not simply referenced from it). The new tree must contain all 
	 * the values of the given tree, but not necessarily in the same structure.
	 * 
	 * @param avlTree - an AVL tree,
	 */
	public AvlTree(AvlTree avlTree){
		
		this.bstTree = new BstTree();
		for (int number : avlTree)
			this.add(number);
	}

	/**
	 * Calculates the minimum number of Nodes in AVL tree of height h.
	 * 
	 * @param h - height of the tree (a non-negative number).
	 * @return the minimum number of nodes in the AVL tree of the given height.
	 */
	public static int findMinNodes(int h){
		
		if (h==0)
			return 1;
		if (h==1)
			return 2;
		return (findMinNodes(h-1)+findMinNodes(h-2)+1);
	}
	
	/**
	 * Add a new node with the given key to the tree.
	 * 
	 * @param newValue - the value of the new node to add.
	 * @return true if the value to add is not already in the tree and it was successfully added.
	 * false otherwise.
	 */
	 public boolean add(int newValue){
		 
		 IntegerBstNode newNode = this.bstTree.add(newValue);
		 
		 if (newNode == null) // means the value didn't add.
			 return false;
		 
		 checkValidAvL(newNode, CHECK_AFTER_ADDING);
		 return true; 
	 }
	
	/**
	 * Check whether the tree contains the given input value.
	 * 
	 * @param searchVal -  the value to search for.
	 * @return the depth of the node (0 for the root) with the given value if it was found in the tree,
	 * -1 otherwise.
	 */
	public int contain(int searchVal){
		
		return this.bstTree.contain(searchVal);
	}
	
	
	/**
	 * Removes the node with the given value from the tree, if it exist.
	 * 
	 * @param toDelete - the value to remove from the tree.
	 * @return true if the given value was found and deleted, false otherwise.
	 */
	 public boolean delete(int toDelete){
		 
		 boolean isDeletRoot = false; // If deleting root in one size tree means no father to come back! 
		 
		 if (this.bstTree.getHead() != null && (toDelete == this.bstTree.getHead().getValue()))
			 isDeletRoot = true;
		 
		 IntegerBstNode parentItemDeleted = this.bstTree.delete(toDelete);
		 
		 if (parentItemDeleted == null && !isDeletRoot)
			 return false;
	 
		 checkValidAvL(parentItemDeleted, CHECK_AFTER_DELETE); 
		 return true;
		 
	 }
	 
		/*
		 *  Check if the tree is valid or need to fix after adding and deleting.
		 */
		private void checkValidAvL(IntegerBstNode startCheckFromHere, int afterDeletionOrAdding){
		
			IntegerBstNode currentNode = startCheckFromHere;
			
			while(currentNode != null){
						
					int whatVaiolation = AvlOutOfBalance.isAvlBrokeHere(currentNode);
					
					if (whatVaiolation != AvlOutOfBalance.NO_VAIOLATION){
						boolean isRightSon = (currentNode.getParent()==null)? true : BstTree.isRightChild(currentNode);
						IntegerBstNode fixNode = null;

						// Check what case of braking we are:
						switch (whatVaiolation){
								
							case AvlOutOfBalance.VAIOLATION_RR:
								fixNode = AvlOutOfBalance.fixRRviolation(currentNode);
								break;
									
							case AvlOutOfBalance.VAIOLATION_RL:
								fixNode = AvlOutOfBalance.fixRLviolation(this.bstTree.getHead(), currentNode);
								break;
										
							case AvlOutOfBalance.VAIOLATION_LL:
								fixNode = AvlOutOfBalance.fixLLviolation(currentNode);
								break;
										
							case AvlOutOfBalance.VAIOLATION_LR:
								fixNode =  AvlOutOfBalance.fixLRviolation(this.bstTree.getHead(), currentNode);
								break;
						}
						if (currentNode == this.bstTree.getHead())
							this.bstTree = new BstTree(fixNode, this.bstTree.size());	
						else
							AvlOutOfBalance.updateParentAfterFixing(fixNode, isRightSon);
						
						this.bstTree.updateHeights(fixNode);
						
						// It's sure that after adding there will only one violation!
						if (afterDeletionOrAdding == CHECK_AFTER_ADDING)
							break;	
					}
					
					currentNode = currentNode.getParent();
				}
			}
	 
	
	/**
	 * @return the number of nodes in the tree.
	 */
	public int size(){
		
		return this.bstTree.size();
	}
	
	/**
	 * @return an iterator of the AvlTree. The returned iterator over the tree nodes in an ascending oreder,
	 * and doe's NOT implement the remove() method.
	 */
	public Iterator<Integer> iterator(){
		
		return new AvlTreeIterator(this.size(), this.bstTree.tree_min(this.bstTree.getHead()));
	}
	

}
