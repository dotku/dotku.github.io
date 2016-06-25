class Speak {
    public static void main(String[] args) {
        // System.out.println("Hello World!"); // Display the string.
        Speak speak = new Speak();
        speak.doIt();
    }

    public static void doIt(){
      
      ApplicationContext ctx=new FileSystemXmlApplicationContext(getClass().getResource("bean.xml").toString());
      Person person=null;
      person = (Person)ctx.getBean("chinese");
      person.sayHello();
      person.sayBye();
      
      person = (Person)ctx.getBean("american");
      person.sayHello();
      person.sayBye();
     }
}
