package ex0;

class Store {
	
	final String DOWN_LINE = "\n";
	final int PRODUCT_NOT_EXISTENT = -1;
	
	final int MAX_NUM_OF_PRODUCT_TYPES = 5;
	int balance;			
	ProductType[] productTypeArray;
	
	/**
	* Constructor.
	*/
	Store() {
		balance = 0;
		productTypeArray = new ProductType[MAX_NUM_OF_PRODUCT_TYPES];

	}
	
	/**
	* String representation of the store.
	* @return String value represent the information of store includes 
	* the balance and the products of the store.
	*/
	String stringRepresentation() {
	
		String dataOfStore = "Store has a balance of " + balance + ", and the following products:";
		for (int i=0; i<productTypeArray.length; i++){
			
			if (productTypeArray[i] != null){
				
				dataOfStore += (DOWN_LINE + productTypeArray[i].stringRepresentation());
			}
		}
		
		return dataOfStore;
	}
	
	/*
	 * Private method that return the place of it in the array.
	 * @param productTypeName; Name of some product.
	 * @return an int value represent the index of the product in store if is not
	 * existent so return -1.
	 */
	private int placeOfProducte(String productTypeName){
		
			for (int i=0; i<productTypeArray.length; i++){
			
				if ((productTypeArray[i] != null) && 
						(productTypeArray[i].name == productTypeName)){
					return i;
				}
			}
			return PRODUCT_NOT_EXISTENT;
		
	}
	
	/**
	* Check if product is in store.
	* @param productTypeName; The name of product.
	* @return true if it is in store, false otherwise.
	*/
	boolean sellsProductsOfType(String productTypeName){
		
		if (placeOfProducte(productTypeName) != PRODUCT_NOT_EXISTENT){
			return true;
		}
		return false;
		
	}
	
	/**
	* Remove a product if it is in store.
	* @param productTypeName; The name of product.
	* @return true if the product remove, false otherwise.
	*/
	boolean removeProductTypeFromStore(String productTypeName){
		
		int indexOfProdoct = placeOfProducte(productTypeName);
		
		if (indexOfProdoct !=  PRODUCT_NOT_EXISTENT) {
			
			productTypeArray[indexOfProdoct] = null;
			return true;
			
		}
		return false;
	}
	
	/**
	* Remove a product if it is in store.
	* @param productType; The product optional to add.
	* @return true if the product was add to the store, false otherwise.
	*/
	boolean addProductType(ProductType productType) {
				
		for (int i=0; i<productTypeArray.length; i++){
			
			// Checks if there is a place for the new product
			if (productTypeArray[i] == null){
				productTypeArray[i] = productType;
				return true;
			}
		}
		return false;
				
	}

	/**
	* Do a purchase (update balance) if concerning the efforts of the customer.
	* @param customer; The customer who wish to do the purchase.
	* @param productTypeName; The product the customer wish to buy.
	* @param quantity; The quantity of this product the customer wish to buy.
	* @return The actual number of products purchased of the product.
	*/
	int makePurchase(Customer customer, String productTypeName, int quantity){
		
		// Check if quantity is valid number and if product it's in store
		if (quantity<=0 || !(sellsProductsOfType(productTypeName))){
			return 0;
		}
		
		ProductType prodouctLikeToBuy = productTypeArray[placeOfProducte(productTypeName)];
		
		// Check if the quantity is more than the customer can affords
		if (!customer.canAfford(quantity, prodouctLikeToBuy)){
			quantity = customer.maximumAffordableQuantity(prodouctLikeToBuy);
		}
		
		customer.makePurchase(quantity, prodouctLikeToBuy);
		balance += (prodouctLikeToBuy.profitPerUnit() * quantity);
		return quantity;
		
	}

}
