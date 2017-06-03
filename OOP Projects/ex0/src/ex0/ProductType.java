package ex0;

/**
* Represents a product type the store may contains.
* @author Yoni Mantzur
* @see Store
* @see Customer
*/
public class ProductType {

	String name;
	int storePrice;
	int customerPrice;
	
	/**
	* Constructor.
	* @param productName; The name of the product
	* @param productStorePrice; The price of the product the store needs 
	                                        to pay for
	* @param productCustomerPrice; The price of the product the customer needs 
	                                        to pay for
	*/
	ProductType(String productName, int productStorePrice, 
	                                int productCustomerPrice) {
		
		name = productName;
		storePrice = productStorePrice;
		customerPrice = productCustomerPrice;		

	}
	
	/**
	* String representation of the product type, for e.g: 
	* product name:"Apple", store price: 50 and customer price:80, will shown: 
	* "[Apple,50,80]".
	* @return String value represent the information of product.
	*/
	String stringRepresentation() {
	
		return('['+name+','+storePrice+','+customerPrice+']');
		
	}
	
	/**
	*The profit per unit for this product type.
	*@return int value represent the profit.
	*/
	int profitPerUnit() {
		
		return customerPrice - storePrice;
	}

}