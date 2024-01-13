const getHumanDate = (datetime) => {
  var newDate = new Date(datetime);
  return newDate.toUTCString();
};

export default getHumanDate;
