using GL.Domain.Entities;
using GL.Application.DTOs;
using System;
using System.Collections.Generic;

namespace GL.Application.Services
{
    public class PurchaseService
    {
        private readonly IPurchaseRepository _repository;

        public PurchaseService(IPurchaseRepository repository)
        {
            _repository = repository;
        }

        public Transaction CreatePurchaseEntry(PurchaseRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = $"Mua hàng từ {request.SupplierId}"
            };

            decimal netAmount = request.SubTotal;
            decimal vatAmount = request.SubTotal * request.VatRate;
            string cashAccount = request.PaymentMethod == "CASH" ? "1111" : 
                              request.PaymentMethod == "BANK_TRANSFER" ? "112" : "331";

            string inventoryAccount = !string.IsNullOrEmpty(request.InventoryAccount) 
                ? request.InventoryAccount : "156";

            transaction.AddLine(inventoryAccount, netAmount, 0, "Hàng mua");
            
            if (vatAmount > 0)
            {
                transaction.AddLine("1331", vatAmount, 0, "VAT đầu vào");
            }

            transaction.AddLine(cashAccount, 0, netAmount + vatAmount, 
                request.PaymentMethod == "CASH" ? "Tiền mặt" : 
                request.PaymentMethod == "BANK_TRANSFER" ? "TK Ngân hàng" : "Phải trả NCC");

            return transaction;
        }

        public Transaction CreateDirectExpenseEntry(PurchaseRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = $"Chi phí mua hàng từ {request.SupplierId}"
            };

            decimal netAmount = request.SubTotal;
            decimal vatAmount = request.SubTotal * request.VatRate;
            string expenseAccount = !string.IsNullOrEmpty(request.ExpenseAccount) ? request.ExpenseAccount : "621";

            transaction.AddLine(expenseAccount, netAmount, 0, "Chi phí");
            
            if (vatAmount > 0)
            {
                transaction.AddLine("1331", vatAmount, 0, "VAT đầu vào");
            }

            string cashAccount = request.PaymentMethod == "CASH" ? "1111" : "331";
            transaction.AddLine(cashAccount, 0, netAmount + vatAmount, "Thanh toán");

            return transaction;
        }

        public Transaction CreateFreightEntry(FreightRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = "Chi phí vận chuyển"
            };

            string freightAccount = !string.IsNullOrEmpty(request.FreightAccountCode) 
                ? request.FreightAccountCode : "1562";

            transaction.AddLine(freightAccount, request.FreightAmount, 0, "CP vận chuyển");
            transaction.AddLine("331", 0, request.FreightAmount, "Phải trả");

            return transaction;
        }

        public Transaction CreatePurchaseDiscountEntry(PurchaseDiscountRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = request.IsCreditNote 
                    ? $"Giảm giá mua hàng - Phiếu tính giá" 
                    : $"Chiết khấu mua hàng"
            };

            decimal returnAmount = request.DiscountAmount;

            if (request.DiscountType == "PURCHASE_DISCOUNT")
            {
                transaction.AddLine("331", returnAmount, 0, "Phải trả NCC");
                transaction.AddLine("5211", 0, returnAmount, "Giảm giá mua hàng");
            }
            else
            {
                transaction.AddLine("331", returnAmount, 0, "Phải trả NCC");
                transaction.AddLine("1111", 0, returnAmount, "Tiền mặt");
            }

            return transaction;
        }

        public Transaction CreatePurchaseReturnEntry(PurchaseReturnRequest request)
        {
            var transaction = new Transaction
            {
                Id = request.TransactionId ?? Guid.NewGuid().ToString(),
                Date = request.TransactionDate,
                Description = $"Trả hàng mua - {request.OriginalPurchaseId}"
            };

            string inventoryAccount = !string.IsNullOrEmpty(request.InventoryAccount) 
                ? request.InventoryAccount : "156";

            decimal totalReturn = request.ReturnAmount + request.VatAmount;

            if (request.VatAmount > 0 && request.IsVatDeductible)
            {
                transaction.AddLine("331", totalReturn, 0, "Phải trả NCC");
                transaction.AddLine(inventoryAccount, 0, request.ReturnAmount, "Nhập lại kho");
                transaction.AddLine("1331", 0, request.VatAmount, "Giảm VAT đầu vào");
            }
            else
            {
                transaction.AddLine("331", request.ReturnAmount, 0, "Phải trả NCC");
                transaction.AddLine(inventoryAccount, 0, request.ReturnAmount, "Nhập lại kho");
            }

            return transaction;
        }

        public bool ValidateTransaction(Transaction transaction)
        {
            return transaction.IsBalanced;
        }
    }
}