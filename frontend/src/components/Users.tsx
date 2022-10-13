import * as React from 'react';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import { User } from "./User";

interface Column {
  id: 'username' | 'full_name' | 'email' ;
  label: string;
  minWidth?: number;
  align?: 'right';
  format?: (value: number) => string;
}

const columns: readonly Column[] = [
  { id: 'username', label: 'username', minWidth: 170 },
  { id: 'full_name', label: 'full_name', minWidth: 170 },
  { id: 'email', label: 'email', minWidth: 170 },
];


export function Users() {
  let [loading, setLoading] = React.useState(true);
  let [users, setUsers] = React.useState<User[]>([]);
  
    React.useEffect(() => {
      setLoading(true);
      const fetchData = async () => {
        const response = await fetch("http://localhost:8080/users");
        const newData = await response.json();
        setUsers(newData);
        setLoading(false);
      };
  
      fetchData();
    }, []);
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  return (
    <Paper sx={{ width: '100%', overflow: 'hidden' }}>
      <TableContainer sx={{ maxHeight: 440 }}>
        <Table stickyHeader aria-label="sticky table">
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell
                  key={column.id}
                  align='center'
                  style={{ minWidth: column.minWidth,}}
                >
                  {column.label}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {!loading
            ? users
            .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
            .map((user: User) => {
                return (
                  <TableRow hover role="checkbox" tabIndex={-1} key={user.id}>
                    {columns.map((column) => {
                      const value = user[column.id];
                      return (
                        <TableCell key={column.id} align={column.align}>
                          {column.format && typeof value === 'number'
                            ? column.format(value)
                            : value}
                        </TableCell>
                      );
                    })}
                  </TableRow>
                );
              })
              : null}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[10, 25, 100]}
        component="div"
        count={users.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Paper>
  );
}