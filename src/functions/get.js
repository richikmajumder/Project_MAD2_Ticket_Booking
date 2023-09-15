export async function get(url){
  const response = await fetch(url,{headers: {
        'Content-type':'application/json',
        Authorization: `Bearer ${localStorage.getItem('authToken')}`
      }});
      try{
  if(response.ok){
    const data = await response.json()
    console.log(data)
    //console.log(this.venuelist)
    //alertify.alert(data.message)
    return data;
  }
  else{
    console.log(response.statusText)
    console.log(response.message)
    //alertify.alert(response.statusText)
  }}
  catch(error){
    console.log(error);
    //alertify.alert(error)
  }

}