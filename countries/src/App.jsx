import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient("https://rdoctmnuxjszrpqukyns.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJkb2N0bW51eGpzenJwcXVreW5zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjM3ODg3MDIsImV4cCI6MjAzOTM2NDcwMn0.GbGOaFkmIZ20IWo8mjxwrfpdFzpo2XE-pOwN22fpOgc");

function App() {
  const [countries, setCountries] = useState([]);

  useEffect(() => {
    getCountries();
  }, []);

  async function getCountries() {
    const { data } = await supabase.from("countries").select();
    setCountries(data);
  }

  return (
    <ul>
      {countries.map((country) => (
        <li key={country.name}>{country.name}</li>
      ))}
    </ul>
  );
}

export default App;