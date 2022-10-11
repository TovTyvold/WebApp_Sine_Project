const sendData = async (uri: string, data: Array<Object>) => {
    console.log(JSON.stringify(data));

    try {
      let response = await fetch(uri, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const responseData = await response.json();
      return responseData.points;
    } catch (error) {
      console.log(error);
    }
}

export default sendData;