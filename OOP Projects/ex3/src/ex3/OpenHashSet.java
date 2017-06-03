package ex3;

/**
 * Implement Hash set using the open method.
 * 
 * @see SimpleHashSet
 * @author YONI
 *
 */
public class OpenHashSet extends SimpleHashSet {

	/* Final string that tells the cell was 'cleaned' */
	private static final String ITEM_DELETED = new String("DELETED_ITEM");
	
	/* The probing method*/
	private static final int PROBING = 2;
	
	// The hash table.
	private String[] hashTable;
	
	private int capacityTable;
	// Tells if the table in rehash state
	private boolean reHashStatus;
	//Charge where to put the current item checked / where the place the current item checked
	private int placeToPut, PlaceToDelete;
	//Charge if the current item checked is in table
	private boolean isInList;
	
	/**
	 * Constructor.
	 */
	public OpenHashSet(){
		
		super();
		this.reHashStatus = false;
	}
	
	/**
	 * Constructor.
	 * 
	 * @param - upperLoadFactor - the upper limit of loading.
	 * @param - lowerLoadFactor - the lower limit of loading. 
	 */
	public OpenHashSet(float upperLoadFactor, float lowerLoadFactor) {
		
		super(upperLoadFactor, lowerLoadFactor);
		this.reHashStatus = false;
	}
	
	/**
	 * Constructor.
	 * 
	 * @param data - list of Strings wants to add to the set.
	 */
	public OpenHashSet(String[] data) {
		// TODO Auto-generated constructor stub
		
		super(data);
		this.reHashStatus = false;

	}
	
	@Override
	/**
	 * Initialize the String Table.
	 */
	protected void initializeHashTable(int capacity){
	
		this.capacityTable = capacity;
		this.hashTable =  new String[this.capacityTable];
	
	}

	/**
	 * Check if need to rehash and done it case case. 
	 * @param  goalCapacity - the size of the table after rehash (means came from add or delete) 
	 * @param reHashStatus - tells if it call to rehash in current rehash.
	 * @return true if done rehash
	 */
	protected boolean isRehashNeed(int goalCapacity, boolean reHashStatus){

		if (super.isReHashNeed(goalCapacity, this.reHashStatus)){
			
			this.reHashStatus = true;
			
			// Resize the table.
			String[] oldHashTable = this.hashTable;
			this.initializeHashTable(goalCapacity);
			
			for(String item : oldHashTable ){
				if (item == null || item == ITEM_DELETED)	
					continue;
				this.add(item);	
			}
			
			this.reHashStatus = false;
			return true;
		}
		
		return false;
	}
	
	
	
	@Override
	public boolean contains(String searchVal) {
		
		findPlace(searchVal);
		return (this.isInList); // using findPlace function
	}
	
	/*
	 * Charge on checking what place to put the item. If the item is already in the table, return is place
	 * in negative.
	 */
	private void findPlace(String item){
		
		int findPlace =  super.getHashNumber(item);;
		// As we have been told, need to run on cells in the table, n times at most. 
		for (int i = 1; i <=this.capacityTable; i++){ 
			
			// Using '==' for compare to the 'delete' flag.
			if (this.hashTable[findPlace] == null){
				this.placeToPut = findPlace;
				this.isInList = false;
				break;
			}
			
			// And then equals for the contains. 
			else if (this.hashTable[findPlace].equals(item)){
				// I don't know if the function called for deletion or contain but it doesn't mind
				// because the contain function will call each time!
				this.isInList = true;
				this.PlaceToDelete = findPlace;
				break;
			}			
			
			findPlace = (findPlace + (i+i*i)/PROBING)&(this.capacityTable - 1); // Open hash
		}
		
	
	}
	
	@Override
	public boolean add(String newValue){
				
		if (!super.add(newValue))
			return false;
		
		hashTable[this.placeToPut] = newValue;
		isRehashNeed(this.capacityTable*PROBING, this.reHashStatus);
		return true;
	}
	
	@Override
	public boolean delete(String toDelete) {
		
		if (!super.delete(toDelete))
			return false;
		
		// 'Mark' as deleted.
		this.hashTable[this.PlaceToDelete] = ITEM_DELETED;
		isRehashNeed(this.capacityTable /PROBING, this.reHashStatus);
		return true;	
	}
	

	@Override
	public int capacity() {
		
		return this.capacityTable;
	}
	
}

