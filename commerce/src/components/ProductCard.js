const ProductCard = ({ product }) => {
    return (
        <div className="product-card">
            <h3>{product.Name}</h3>
            <p>{product.Price}</p>
            <p>{product.Link}</p>
            <div className="discount">{product.Discount}</div>
        </div>
    )
}


export default ProductCard;