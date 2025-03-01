### E-commerce Database Schema & API Routes (Pseudocode)

#### Database Schema (dbdiagram.io format)

```sql
Table User {
    ID String [pk]
    Email String [unique]
    Password String
    IsEmailVerified Boolean
    SocialAuthProvider String // Google, Facebook, etc.
    RegistrationDate DateTime
    IsDeleted Boolean
}

Table UserDetails {
    UserID String [ref: > User.ID]
    FirstName String
    LastName String
    Mobile String
    ProfileImage String
    UpdatedAt DateTime
}

Table Address {
    ID String [pk]
    UserID String [ref: > User.ID]
    Street String
    City String
    State String
    Country String
    PostalCode String
    IsPrimary Boolean
}

Table Category {
    ID String [pk]
    Name String
    ParentID String [ref: > Category.ID, null]
}

Table ProductCategory {
    ProductID String [ref: > Product.ID]
    CategoryID String [ref: > Category.ID]
    Indexes {
        (ProductID, CategoryID) [pk]
    }
}

Table Product {
    ID String [pk]
    Name String
    Description Text
    Brand String
    Images String[]
    CreatorID String [ref: > User.ID]
    Shaders JSON
    RoyaltyPercentage Decimal
    Tags String[]
    Rating Decimal
    ReviewsCount Int
    WarehouseID String [ref: > Warehouse.ID]
    use_stock_price BOOLEAN DEFAULT FALSE


    Indexes {
        Name
        Brand
        CreatorID
        (Name, Brand) [name: 'idx_product_search']
    }
}

Table ProductVariant {
    ID String [pk]
    ProductID String [ref: > Product.ID]
    Size String
    Color String
    Price Decimal
    Stock Int

    Indexes {
        ProductID
        (ProductID, Size, Color) [unique]
    }
}

Table Model3D {
    ID String [pk]
    UserID String [ref: > User.ID]
    ProductID String [ref: > Product.ID, null]
    ModelType String
    ModelURL String
    CreatedAt DateTime
}

Table ProductCoupon {
    ID String [pk]
    ProductID String [ref: > Product.ID]
    Discount Decimal
    ExpiryDate DateTime
}

Table ProductOffer {
    ID String [pk]
    Title String
    ProductIDs String[]
    Discount Decimal
    ExpiryDate DateTime
}

Table Order {
    ID String [pk]
    UserID String [ref: > User.ID]
    OrderDate DateTime
    OrderStatus String // Processing, Shipped, Delivered, Canceled
    ShippingAddressID String [ref: > Address.ID]
    BillingAddressID String [ref: > Address.ID]
    TotalAmount Decimal
    PaymentStatus String // Paid, Failed, Refunded
    CanModify Boolean
    TrackingID String
    EstimatedDelivery DateTime
    CancellationReason String // Added for order cancellation tracking

    Indexes {
        UserID
        OrderDate
        OrderStatus
        PaymentStatus
        (UserID, OrderDate) [name: 'idx_user_orders']
    }
}

Table OrderItem {
    ID String [pk]
    OrderID String [ref: > Order.ID]
    ProductID String [ref: > Product.ID]
    VariantID String [ref: > ProductVariant.ID, null]
    Quantity Int
    DiscountedPrice Decimal
    AppliedCouponID String [ref: > ProductCoupon.ID, null]
    AppliedOfferID String [ref: > ProductOffer.ID, null]
}

Table ReturnRequest {
    ID String [pk]
    UserID String [ref: > User.ID]
    OrderID String [ref: > Order.ID]
    RefundStatus String
    Items String[]
    Quantities Int[]
    ReturnReason String
    CreatedAt DateTime
    ResolvedAt DateTime
    ReturnStatus String // Pending, Approved, Rejected
    RefundAmount Decimal
}

Table Transaction {
    ID String [pk]
    OrderID String [ref: > Order.ID]
    StoreTransactionID String [unique] // External payment transaction ID
    TransactionType String
    TotalAmount Decimal
    Date DateTime
}

Table Royalty {
    ID String [pk]
    CreatorID String [ref: > User.ID]
    SalesAmount Decimal
    RoyaltyEarned Decimal
    LastUpdated DateTime
}

Table Analytics {
    ID String [pk]
    UserID String [ref: > User.ID]
    Action String
    ProductID String [ref: > Product.ID]
    Timestamp DateTime
    DeviceInfo JSON
    Location String
    SessionID String

    Indexes {
        ProductID
        UserID
        Action
        Timestamp
        (ProductID, Action) [name: 'idx_product_analytics']
    }
}

Table Review {
    ID String [pk]
    UserID String [ref: > User.ID]
    ProductID String [ref: > Product.ID]
    OrderID String [ref: > Order.ID, null]
    Rating Int
    Title String
    Comment Text
    Images String[]
    CreatedAt DateTime
    UpdatedAt DateTime
    Helpful Int
    ReportCount Int
    IsVerifiedPurchase Boolean

    Indexes {
        ProductID
        UserID
        Rating
        (ProductID, Rating) [name: 'idx_product_rating']
    }
}

Table Wishlist {
    ID String [pk]
    UserID String [ref: > User.ID]
    ProductID String [ref: > Product.ID]
    AddedAt DateTime

    Indexes {
        UserID
        (UserID, ProductID) [unique]
    }
}

Table Cart {
    ID String [pk]
    UserID String [ref: > User.ID]
    ProductID String [ref: > Product.ID]
    VariantID String [ref: > ProductVariant.ID, null]
    Quantity Int
    AddedAt DateTime
    UpdatedAt DateTime

    Indexes {
        UserID
        (UserID, ProductID) [unique]
    }
}

Table Warehouse {
    ID String [pk]
    Name String
    Location JSON
    ContactInfo JSON
}

Table StockMovement {
    ID String [pk]
    ProductID String [ref: > Product.ID]
    VariantID String [ref: > ProductVariant.ID, null]
    WarehouseID String [ref: > Warehouse.ID]
    Quantity Int
    Reason String
    ReferenceID String
    Timestamp DateTime

    Indexes {
        ProductID
        WarehouseID
        Timestamp
        (ProductID, Timestamp) [name: 'idx_product_stock_history']
    }
}

Table UserLoyaltyPoints {
    UserID String [ref: > User.ID, pk]
    Points Int
    Tier String
    LastUpdated DateTime
}

Table PointsTransaction {
    ID String [pk]
    UserID String [ref: > User.ID]
    Points Int
    Reason String
    ReferenceID String
    Timestamp DateTime

    Indexes {
        UserID
        Timestamp
        (UserID, Timestamp) [name: 'idx_user_points_history']
    }
}
```

---

# API Routes & Logic (Pseudocode)

## User Authentication

**POST /register** `{email, password}` → Create user, send verification email
**POST /login** `{email, password}` → Check email verification, generate JWT
**POST /social-login** `{provider, token}` → Authenticate via Google/Facebook
**POST /verify-email** `{token}` → Mark user as verified
**POST /logout** → Invalidate session
**DELETE /delete-account/{userID}** → Soft delete user (isDeleted = TRUE)
**POST /reset-password** `{email}` → Initiate password recovery

## Address Management

**POST /address** `{userID, address}` → Add new address
**PATCH /address/set-primary** `{userID, addressID}` → Set primary address
**DELETE /address/{addressID}** → Remove address

## Category Management

**POST /category** `{name, parentID}` → Create category
**GET /categories** → Fetch category hierarchy
**PATCH /category/{categoryID}** → Update category
**DELETE /category/{categoryID}** → Remove category

## Product Management

**POST /product** `{creatorID, productDetails}` → Create product
**PATCH /product/{productID}** → Update product details
**GET /product/{productID}** → Fetch product details
**DELETE /product/{productID}** → Remove product
**POST /product/review** `{userID, productID, rating, comment}` → Add user feedback
**GET /product/reviews/{productID}** → Fetch all reviews for a product

## 3D Model Management

**POST /model3d** `{userID, modelURL, modelType, productID}` → Upload model
**PATCH /model3d/{modelID}** `{productID}` → Link/unlink a product
**GET /model3d/{productID}** → Fetch all models linked to a product
**DELETE /model3d/{modelID}** → Remove model (if not in use)

## Pricing & Offers

**POST /product-coupon** `{productID, discount, expiry}` → Create coupon
**POST /product-offer** `{productIDs[], discount, expiry}` → Create bundle offer
**GET /price-check** `{cartItems[]}` → Calculate total price with discounts
**PATCH /product/{productID}/toggle-stock-price** `{use_stock_price}` → Toggle stock-based pricing

## Order Management

**POST /order** `{userID, cartItems[], shippingAddress}` → Create order
**PATCH /order/{orderID}** `{modifications}` → Modify order if processing
**PATCH /order/status/{orderID}** `{newStatus}` → Update order status

-   When status changes from "Processing" to "Shipped", automatically set CanModify to FALSE
    **GET /order-history/{userID}** → Fetch all past orders
    **DELETE /order/{orderID}** → Cancel order (if allowed)
    **GET /order/{orderID}/tracking** → Fetch shipment tracking info

## Return & Refund

**POST /return-request** `{userID, orderID, items[], quantities[], returnReason}` → Request return
**PATCH /return/{returnID}** `{status, refundAmount}` → Approve or deny return

## Transaction & Royalty

**GET /transaction-history/{userID}** → Fetch all transactions
**GET /royalty/{creatorID}** → Fetch earnings

## Analytics

**POST /analytics** `{userID, action, productID, deviceInfo, location, sessionID}` → Log action
**GET /analytics/report/{userID}** → Fetch insights for user engagement
**GET /analytics/session/{sessionID}** → Fetch session activity

## Reviews

**POST /review** `{userID, productID, orderID, rating, title, comment, images}` → Create review
**PATCH /review/{reviewID}** `{rating, title, comment, images}` → Update review
**DELETE /review/{reviewID}** → Remove review
**GET /reviews/{productID}** → Fetch all reviews for a product
**POST /review/{reviewID}/helpful** → Mark review as helpful
**POST /review/{reviewID}/report** → Report inappropriate review

## Wishlist Management

**POST /wishlist** `{userID, productID}` → Add product to wishlist
**GET /wishlist/{userID}** → Fetch user's wishlist
**DELETE /wishlist/{userID}/{productID}** → Remove product from wishlist

## Cart Management

**POST /cart** `{userID, productID, quantity}` → Add product to cart
**PATCH /cart/{userID}/{productID}** `{quantity}` → Update product quantity
**GET /cart/{userID}** → Fetch user's cart
**DELETE /cart/{userID}/{productID}** → Remove product from cart
**DELETE /cart/{userID}** → Clear entire cart

## Warehouse & Inventory Management

**POST /warehouse** `{name, location, contactInfo}` → Add new warehouse
**GET /warehouses** → List all warehouses
**PATCH /warehouse/{warehouseID}** → Update warehouse details
**POST /stock-movement** `{productID, warehouseID, quantity, reason, referenceID}` → Record stock change
**GET /stock-history/{productID}** → Fetch product stock movement history
**GET /inventory-report/{warehouseID}** → Generate inventory report

## Loyalty & Rewards

**GET /loyalty-points/{userID}** → Check user's points balance and tier
**POST /loyalty-points/earn** `{userID, points, reason, referenceID}` → Award points
**POST /loyalty-points/redeem** `{userID, points, reason, referenceID}` → Redeem points
**GET /loyalty-points/history/{userID}** → Fetch points transaction history
**GET /loyalty-tier/benefits/{tier}** → Fetch tier-specific benefits
