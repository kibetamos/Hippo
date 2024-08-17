
import React, { useEffect } from 'react'
import supabase from '../config/supabaseClient';

export default function Home() {
    const [fetchError, setFetchError] = React.useState(null);
    const [products, setProducts] = React.useState(null)

    useEffect(() => {
        // const fetchProducts = async () => {
        //     const{ data, error } await supabase
        //     .from()
        // }
    })

  return (
    <div>Home
    </div>
  )
}
