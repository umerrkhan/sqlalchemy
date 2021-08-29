import sqlalchemy
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

engine = create_engine("sqlite:///test.db")
session = sessionmaker(bind=engine)() # This is will evaluate it as function ()
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    username = Column(sqlalchemy.String, primary_key=True)
    password = Column(sqlalchemy.String)
    def __init__(self, username, password):
        self.username = username
        self.password = password
    def __repr__(self):
        return "<TableName:User(Username='%s', Password='%s'')>" % (self.username, self.password)

class emp(Base):
    __tablename__ = "emp"
    empno = Column(sqlalchemy.Integer, primary_key=True)
    ename = Column(sqlalchemy.String)
    sal = Column(sqlalchemy.String)
    deptno = Column(sqlalchemy.Integer)

    def __init__(self, empno, ename, sal, deptno):
        self.empno = empno
        self.ename = ename
        self.sal = sal
        self.deptno = deptno
    def __repr__(self):
        return "<TableName:emp(empno='%s', ename='%s', sal='%s', deptno='%s' ')>" % (self.empno, self.ename, self.sal, self.deptno)

def main() -> None:
    #Insert_Into_Table_Values()
    pass_sql_stament()




def pass_sql_stament():
    print(55 * "-")
    sql_stmt = text("Select * From emp")
    result = session.query(emp).from_statement(sql_stmt).all()
    print(result)

    print(55 * "--")
    result = session.query(emp).filter(emp.ename.like("%are%")).all()
    print(result)


    print(55 * "--")
    result = session.query(emp).filter(text("empno>3")).all()
    print(result)


    print(55 * "==")
    sql_stmt = text("Select deptno, sum(sal) as sal From emp Group by sal")
    sql_stmt = sql_stmt.columns(emp.deptno, emp.sal)
    result = session.query(emp.deptno, emp.sal).from_statement(sql_stmt).all()
    print(result)


    print(55 * "==")
    result = session.query( emp.empno, emp.ename ,User.password ).filter(emp.empno==User.username).all()
    print(result)




def update_table():
    result = session.query(User).filter_by(username='umer').first()
    result.password = "N1strongpassword"
    print(session.dirty)
    print(session.new)
    session.commit()


def Select_Star_from_table_where() -> None:
    result = session.query(User).filter_by(username='1000').first()
    print(result)


def Select_Star_from_table(option:int) -> None:
    if option == 1:
        all_user = session.query(User).all()
        print(all_user)
    else:
        #print only selected columns
        for row in session.query(emp, emp.empno, emp.ename,emp.sal).order_by(emp.sal):
            print(row.empno, row.ename, row.sal)

def Insert_Into_Table_Values() -> None:
    # Option 1
    # Inserting Data in the DB one at a time
    One_Record = User("1", "pwd1")
    session.add(One_Record)
    session.commit()

    # Option 2
    # Inserting multiple records once at a time
    Multiple_Records = [User('2', 'pwd-11'), \
                        User('3', 'pwd-12'), \
                        User('4', 'pwd-13'), \
                        User('5', 'pwd-14')]
    session.add_all(Multiple_Records)
    session.commit()

    Employee = [emp(1, "Karen", 1, 10), \
                emp(2, "Alex", 1, 10), \
                emp(3, "John", 2, 20), \
                emp(4, "Parker", 2, 20), \
                emp(5, "Judy", 3, 30)
                ]

    session.add_all(Employee)
    session.commit()


if __name__ == '__main__':
    main()
