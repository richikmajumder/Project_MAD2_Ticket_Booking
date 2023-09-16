import alertify from 'alertifyjs';
export async function update(url,payload,router){
    const authToken = localStorage.getItem('authToken');
    const response = await fetch(url,{
    method:'POST',
    headers:{'Content-Type': 'application/json',
              Authorization: `Bearer ${authToken}`,},
    body:JSON.stringify(payload)
  });
  try{
    if(response.ok){
      const data = await response.json()
      console.log(data)
      alertify.alert(data.message)
    }
    else{
      console.log(response.statusText)
      const data = await response.json()
      console.log(data)
      alertify.alert(response.statusText)
      if(data.message==='Token has expired' || data.message==='Token is missing' || data.message==='Token is invalid'){
        router.push('/signin');
      }
    }}
    catch(error){
      //console.log(error,1);
      alertify.alert(error);
      //this.$router.push('/signin');
      
    }
  }