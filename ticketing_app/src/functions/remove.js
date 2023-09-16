import alertify from 'alertifyjs';
export async function remove(url){
  const response = await fetch(url,{
    method:'DELETE',
    headers:{
      Authorization: `Bearer ${localStorage.getItem('authToken')}`}});
    try{
      if(response.ok){
        const data = await response.json()
        alertify.alert(data.message)
      }
      else{
        console.log(response.statusText)
        if(response.message==='Token is missing' || response.message==='Token has expired' || response.message==='Token is invalid'){
          this.$router.push('/signin');
        }
      }}
      catch(error){
        console.log(error);     
    }
  }

/*export async function remove(payload,url){
    const response = await fetch(url,{
      method:'DELETE',
      headers:{'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('authToken')}`},
      body: JSON.stringify(payload)});
      try{
        if(response.ok){
          const data = await response.json()
          alertify.alert(data.message)
        }
        else{
          console.log(response.statusText)
          if(response.message==='Token is missing' || response.message==='Token has expired' || response.message==='Token is invalid'){
            this.$router.push('/signin');
          }
        }}
        catch(error){
          console.log(error);     
      }
    }*/

