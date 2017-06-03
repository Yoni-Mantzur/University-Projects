package ex0;

/**
* Represents a customer that wants to buy products from store.
* @author Yoni Mantzur
* @see Store
* @see ProductType
*/
public class Customer {

	final String DOWNLINE = "\n";
	
	String name;
	String address;
	int balance;
	String log;
	
	/**
	* Constructor.
	* @param customerName; The name of customer.
	* @param customerAddress; The address of the customer 
	* @param customerBalance; The balance of the customer
	*/
	Customer(String customerName, String customerAddress, int customerBalance){

		name = customerName;
		address = customerAddress;
		balance = customerBalance;
		
		// The purchases log of the customer
		log = "Shopping log for customer:" + name;
		
	}
	

	
	/**
	* String representation of the costumer informations, for e.g: 
	* customer name:"Yoni", address: Jerusalem and balance:80, will shown: 
	* "[Yoni,Jerusalem,80]".
	* @return String value represent the information of customer.
	*/
	String stringRepresentation(){
		
		return('['+name+','+address+','+balance+']');
	}
	
	/*
	 * Private method calculate the price of singular purchase.
	 * @param quantity; The quantity of some product the customer wants.
	 * @param productType; The product the customer wants.
	 * @return the calculate of the price.
	 */
	private int priceOfPurchase(int quantity, ProductType productType){
		
		
		return (productType.customerPrice)*(quantity);
	}
	
	/**
	* Checks whether this customer can afford to pay the purchase.
	* @param quantity; The quantity of some product the customer wants.
	* @param productType; The product the customer wants.
	* @return True if the customer can afford the purchase, false otherwise.
	*/
	boolean canAfford(int quantity, ProductType productType){
		
		// Check the total price
		int priceOfPurchase = priceOfPurchase(quantity, productType);
		
		if (priceOfPurchase <= balance && priceOfPurchase > 0) {
			return true;
		} else {
			return false;
		}
	}
	
	/**
	*The log purchases the customer done.
	*@return String value represent the log of purchases have done.
	*/
	String getPurchaseLog(){
		
		return log;
	}


	/**
	* The maximum quantity the customer can afford to buy from some product.
	* @param productType; The product the customer wants to buy.
	* @return int value represent max quantity from the product can afford.
	*/
	int maximumAffordableQuantity(ProductType productType){

		return balance / productType.customerPrice;

	}

	/**
	* Do the purchase, just if the customer can afford to, and updates the data
	* (balance and log).
	* @param quantity; The quantity of some product the customer wants.
	* @param productType; The product the customer wants.
	*/
	void makePurchase(int quantity, ProductType productType) {
		
		if(canAfford(quantity, productType)){
			
			balance -= priceOfPurchase(quantity, productType);
			log += (DOWNLINE + quantity + " " + productType.name);	
			
		}
		
	}


}
