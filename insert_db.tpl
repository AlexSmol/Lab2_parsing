
<h1><p>Add new advertisement in DB:</p></h1>
<form action="/insert" method="POST">
  <p><label>ID (last number url): <input type="text" size="100" maxlength="100" required name="ID"></label></p>
  <p><label>Name: <input type="text" size="100" maxlength="100" name="Name_Offer"></label></p>
  <p><label>Count room: <input type="text" size="100" maxlength="100" inputmode="numeric" name="Count_room"></label></p>
  <p><label>Address: <input type="text" size="100" maxlength="100" name="Adress"></label></p>
  <p><label>Area: <input type="text" size="100" maxlength="100" inputmode="numeric" name="Area"></label></p>
  <p><label>Price: <input type="text" size="100" maxlength="100" inputmode="numeric" name="Price"></label></p>
  <fieldset>
    <legend>Price currency</legend>
    <p><label> <input type="radio" name="text" required value="Price_currency">RUB</label></p>
    <p><label> <input type="radio" name="text" required value="Price_currency">USD</label></p>
    <p><label> <input type="radio" name="text" required value="Price_currency">EUR</label></p>
  </fieldset>
  <p><label>Phone number:<input type="tel" size="100" maxlength="100" name="Phone_Number"></label></p>
  <p><label>URL: <input type="url" size="100" maxlength="100" required name="Link"></label></p>
 
  <input type="submit" name="save" value="Sumbit AD">
</form>